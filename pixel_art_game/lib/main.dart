import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const PixelArtApp());
}

class PixelArtApp extends StatelessWidget {
  const PixelArtApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF151515),
        appBarTheme: const AppBarTheme(backgroundColor: Color(0xFF222222)),
      ),
      home: const MenuNiveles(),
    );
  }
}

// ------------------------------------------------------------------
// PANTALLA 1: MENÚ
// ------------------------------------------------------------------
class MenuNiveles extends StatelessWidget {
  const MenuNiveles({super.key});

  // Asegúrate de tener estas imágenes en tu carpeta assets
  final List<String> niveles = const [
    'assets/nivel1.png', 
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Galería Pixel Art")),
      body: GridView.builder(
        padding: const EdgeInsets.all(20),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2, crossAxisSpacing: 20, mainAxisSpacing: 20
        ),
        itemCount: niveles.length,
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              Navigator.push(context, MaterialPageRoute(
                builder: (context) => PantallaJuego(rutaImagen: niveles[index], idNivel: "nivel_$index")
              ));
            },
            child: Container(
              decoration: BoxDecoration(
                color: Colors.grey[800],
                borderRadius: BorderRadius.circular(15),
                boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 5)],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Icono genérico si no carga la preview, o la imagen en sí
                  Expanded(child: Padding(
                    padding: const EdgeInsets.all(15.0),
                    child: Image.asset(niveles[index], fit: BoxFit.contain, errorBuilder: (c,e,s) => const Icon(Icons.image, size: 50)),
                  )),
                  Container(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    width: double.infinity,
                    decoration: BoxDecoration(color: Colors.black26, borderRadius: BorderRadius.vertical(bottom: Radius.circular(15))),
                    child: Text("Nivel ${index + 1}", textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

// ------------------------------------------------------------------
// PANTALLA 2: JUEGO (Lógica Mejorada)
// ------------------------------------------------------------------

class PixelInfo {
  final Color colorReal;
  final int indiceColor;
  bool estaPintado;
  PixelInfo(this.colorReal, this.indiceColor, {this.estaPintado = false});
}

class PantallaJuego extends StatefulWidget {
  final String rutaImagen;
  final String idNivel;

  const PantallaJuego({super.key, required this.rutaImagen, required this.idNivel});

  @override
  State<PantallaJuego> createState() => _PantallaJuegoState();
}

class _PantallaJuegoState extends State<PantallaJuego> {
  List<List<PixelInfo>> matriz = [];
  List<Color> paletaColores = [];
  int colorSeleccionadoIndex = 0;
  bool cargando = true;
  bool modoMover = false; // false = Pintar, true = Mover
  
  final TransformationController _transformationController = TransformationController();

  @override
  void initState() {
    super.initState();
    cargarNivel();
  }

  // --- 1. CARGA ROBUSTA ---
  Future<void> cargarNivel() async {
    try {
      final byteData = await rootBundle.load(widget.rutaImagen);
      var imagen = img.decodeImage(byteData.buffer.asUint8List());

      if (imagen == null) return;

      // Reducir si es gigante (Seguridad)
      if (imagen.width > 64 || imagen.height > 64) {
         imagen = img.copyResize(imagen, width: 45);
      }

      // Algoritmo de limpieza de colores (Cuantización simple)
      int redondear(int v) => (v / 20).round() * 20; 
      
      Set<int> coloresSet = {};
      List<Color> paletaTemp = [];

      // Detectar paleta
      for (var p in imagen) {
        if (p.a == 0) continue;
        // Normalizamos el color para agrupar tonos parecidos
        int r = redondear(p.r.toInt());
        int g = redondear(p.g.toInt());
        int b = redondear(p.b.toInt());
        
        // Creamos un entero único para el Set
        int colorInt = Color.fromARGB(255, r, g, b).value;
        
        if (!coloresSet.contains(colorInt)) {
          coloresSet.add(colorInt);
          paletaTemp.add(Color(colorInt));
        }
      }
      // Ordenar por brillo
      paletaTemp.sort((a, b) => b.computeLuminance().compareTo(a.computeLuminance()));
      paletaColores = paletaTemp;

      // Cargar progreso
      SharedPreferences prefs = await SharedPreferences.getInstance();
      List<String>? guardado = prefs.getStringList(widget.idNivel);

      // Crear Matriz
      List<List<PixelInfo>> temp = [];
      int contador = 0;

      for (int y = 0; y < imagen.height; y++) {
        List<PixelInfo> fila = [];
        for (int x = 0; x < imagen.width; x++) {
          final p = imagen.getPixel(x, y);
          
          if (p.a == 0) {
            fila.add(PixelInfo(Colors.white, -1, estaPintado: true));
          } else {
            // Buscamos el color más cercano en la paleta generada
            int r = redondear(p.r.toInt());
            int g = redondear(p.g.toInt());
            int b = redondear(p.b.toInt());
            Color cBuscado = Color.fromARGB(255, r, g, b);
            
            int idx = paletaColores.indexOf(cBuscado);
            if (idx == -1) idx = 0; // Fallback
            
            bool pintado = false;
            if (guardado != null && contador < guardado.length) {
              pintado = guardado[contador] == '1';
            }

            fila.add(PixelInfo(cBuscado, idx, estaPintado: pintado));
          }
          contador++;
        }
        temp.add(fila);
      }

      setState(() {
        matriz = temp;
        cargando = false;
        // Si hay colores, seleccionar el primero
        if (paletaColores.isNotEmpty) colorSeleccionadoIndex = 0;
      });

    } catch (e) {
      print("Error cargando nivel: $e");
    }
  }

  Future<void> guardarProgreso() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String> data = [];
    for (var f in matriz) for (var p in f) data.add(p.estaPintado ? '1' : '0');
    await prefs.setStringList(widget.idNivel, data);
  }

  // --- 2. LÓGICA DE GESTOS E INTERACCIÓN ---

  void _procesarToque(Offset localPosition, {bool esRelleno = false}) {
    if (modoMover || matriz.isEmpty) return;

    // Magia matemática para saber dónde tocamos considerando el Zoom
    final matrix = _transformationController.value;
    final scale = matrix.getMaxScaleOnAxis();
    final translate = matrix.getTranslation();

    double tamanoLienzo = 350.0;
    
    // Deshacer el zoom y la traslación para obtener coordenada real
    double dx = (localPosition.dx - translate.x) / scale;
    double dy = (localPosition.dy - translate.y) / scale;

    double celdaW = tamanoLienzo / matriz[0].length;
    double celdaH = tamanoLienzo / matriz.length;

    int x = (dx / celdaW).floor();
    int y = (dy / celdaH).floor();

    // Validar límites
    if (x >= 0 && x < matriz[0].length && y >= 0 && y < matriz.length) {
      if (esRelleno) {
        _rellenoCruz(x, y); // Lógica nueva sin diagonales
      } else {
        _pintarSimple(x, y);
      }
    }
  }

  void _pintarSimple(int x, int y) {
    PixelInfo p = matriz[y][x];
    if (!p.estaPintado && p.indiceColor == colorSeleccionadoIndex) {
      setState(() {
        p.estaPintado = true;
        HapticFeedback.selectionClick(); // Vibración suave
      });
      guardarProgreso();
    }
  }

  // --- 3. ALGORITMO DE RELLENO EN CRUZ (SIN DIAGONALES) ---
// --- 3. ALGORITMO DE RELLENO EN CRUZ (SIN DIAGONALES) OPTIMIZADO ---
void _rellenoCruz(int startX, int startY) {
  PixelInfo pInicial = matriz[startY][startX];
  
  if (pInicial.estaPintado || pInicial.indiceColor != colorSeleccionadoIndex) return;

  List<Point> cola = [Point(startX, startY)];
  // Usamos una Matriz de booleanos (o un Set de coordenadas) para registrar los visitados.
  // Una matriz de booleanos es más rápido que un Set para accesos por índice.
  List<List<bool>> visitados = List.generate(matriz.length, (y) => 
      List.generate(matriz[0].length, (x) => false));

  bool cambios = false;

  while (cola.isNotEmpty) {
    Point p = cola.removeLast();
    int px = p.x.toInt();
    int py = p.y.toInt();

    // 1. Validar límites y verificar visitado
    if (px < 0 || px >= matriz[0].length || py < 0 || py >= matriz.length || visitados[py][px]) {
      continue;
    }
    
    visitados[py][px] = true; // Marcar como visitado

    PixelInfo actual = matriz[py][px];

    // 2. Verificar condición de pintado
    if (!actual.estaPintado && actual.indiceColor == colorSeleccionadoIndex) {
      setState(() => actual.estaPintado = true);
      cambios = true;

      // Añadir 4 vecinos (Cruz)
      cola.add(Point(px + 1, py)); // Derecha
      cola.add(Point(px - 1, py)); // Izquierda
      cola.add(Point(px, py + 1)); // Abajo
      cola.add(Point(px, py - 1)); // Arriba
    }
  }

  if (cambios) {
    HapticFeedback.heavyImpact();
    guardarProgreso();
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Pixel Art"),
        actions: [
          // Botón opcional para forzar modo mover si se atascan
          IconButton(
            icon: Icon(modoMover ? Icons.pan_tool : Icons.brush),
            color: modoMover ? Colors.blue : Colors.grey,
            onPressed: () => setState(() => modoMover = !modoMover),
          )
        ],
      ),
      body: cargando 
        ? const Center(child: CircularProgressIndicator()) 
        : Column(
            children: [
              Expanded(
                child: Center(
                  // Usamos Listener + GestureDetector para máximo control
                  child: GestureDetector(
                    // 1. Un toque simple pinta un pixel
                    onTapUp: (d) => _procesarToque(d.localPosition, esRelleno: false),
                    
                    // 2. Arrastrar el dedo pinta como un pincel
                    onPanUpdate: (d) {
                      if (!modoMover) _procesarToque(d.localPosition, esRelleno: false);
                    },

                    // 3. Mantener pulsado rellena el área (Flood Fill)
                    onLongPressStart: (d) => _procesarToque(d.localPosition, esRelleno: true),

                    child: InteractiveViewer(
                      transformationController: _transformationController,
                      // TRUCO: Si no estamos en "Modo Mover manual", desactivamos el PAN de 1 dedo
                      // Esto permite que el GestureDetector de arriba capture el arrastre para pintar.
                      // InteractiveViewer sigue funcionando con 2 dedos para Zoom/Pan automáticamente.
                      panEnabled: modoMover, 
                      scaleEnabled: true, 
                      minScale: 0.5,
                      maxScale: 10.0,
                      boundaryMargin: const EdgeInsets.all(300),
                      child: CustomPaint(
                        size: const Size(350, 350),
                        painter: PixelPainter(matriz, colorSeleccionadoIndex),
                      ),
                    ),
                  ),
                ),
              ),

              // --- BARRA DE COLORES MEJORADA ---
              Container(
                height: 110,
                color: const Color(0xFF1E1E1E),
                child: Column(
                  children: [
                    const SizedBox(height: 5),
                    const Text("Mantén pulsado para rellenar área", style: TextStyle(color: Colors.white38, fontSize: 10)),
                    Expanded(
                      child: ListView.builder(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                        itemCount: paletaColores.length,
                        itemBuilder: (context, index) {
                          bool sel = colorSeleccionadoIndex == index;
                          // Calcular restantes
                          int restantes = matriz.expand((r)=>r).where((p)=>p.indiceColor==index && !p.estaPintado).length;
                          bool completado = restantes == 0;
                      
                          if (completado) return const SizedBox(); // Ocultar completados
                      
                          return GestureDetector(
                            onTap: () => setState(() => colorSeleccionadoIndex = index),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 150),
                              margin: const EdgeInsets.symmetric(horizontal: 6),
                              width: sel ? 60 : 45,
                              decoration: BoxDecoration(
                                color: paletaColores[index],
                                shape: BoxShape.circle,
                                border: sel ? Border.all(color: Colors.white, width: 3) : null,
                                boxShadow: sel ? [const BoxShadow(color: Colors.black54, blurRadius: 10)] : null
                              ),
                              child: Center(
                                child: Text(
                                  "${index + 1}",
                                  style: TextStyle(
                                    color: paletaColores[index].computeLuminance() > 0.5 ? Colors.black : Colors.white,
                                    fontWeight: FontWeight.bold,
                                    fontSize: sel ? 20 : 14
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              )
            ],
          ),
    );
  }
}

// --- PINTOR EFICIENTE ---
// SUSTITUYE TODA LA CLASE PixelPainter DEL FINAL POR ESTA:

class PixelPainter extends CustomPainter {
  final List<List<PixelInfo>> pixels;
  final int seleccionado;
  PixelPainter(this.pixels, this.seleccionado);

  @override
  void paint(Canvas canvas, Size size) {
    if (pixels.isEmpty) return;

    final paint = Paint()..style = PaintingStyle.fill;
    final textPainter = TextPainter(textDirection: TextDirection.ltr);

    double w = size.width / pixels[0].length;
    double h = size.height / pixels.length;

    // Pintar fondo base (por si acaso quedan huecos)
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = Colors.grey[900]!);

    for (int y = 0; y < pixels.length; y++) {
      for (int x = 0; x < pixels[y].length; x++) {
        final p = pixels[y][x];
        
        // Usamos un pequeño solapamiento (+0.5) para evitar líneas blancas finas entre pixeles
        Rect rect = Rect.fromLTWH(x * w, y * h, w + 0.5, h + 0.5);

        if (p.estaPintado) {
          // CASO 1: PINTADO -> Color real
          paint.color = p.colorReal;
          canvas.drawRect(rect, paint);
        } else if (p.indiceColor != -1) {
          // CASO 2: NO PINTADO -> Cuadrícula gris y número
          bool esElColorActual = p.indiceColor == seleccionado;
          
          // --- CORRECCIÓN AQUÍ: Usamos grises más claros ---
          paint.color = esElColorActual ? Colors.grey[600]! : Colors.grey[800]!;
          canvas.drawRect(rect, paint);
          
          // Rejilla fina para separar
          canvas.drawRect(rect, Paint()..color = Colors.black26..style = PaintingStyle.stroke..strokeWidth = 0.5);

          // Número
          double fontSize = h * 0.6;
          // Solo dibujamos el número si el tamaño de letra es mínimamente visible (>6)
          // para evitar manchones negros cuando estás muy lejos.
          if (fontSize > 6.0) {
             textPainter.text = TextSpan(
              text: "${p.indiceColor + 1}",
              style: TextStyle(
                color: esElColorActual ? Colors.white : Colors.white54,
                fontSize: fontSize,
                fontWeight: FontWeight.w900 // Negrita extra para que se vea bien
              )
            );
            textPainter.layout();
            textPainter.paint(canvas, rect.center - Offset(textPainter.width/2, textPainter.height/2));
          }
        }
      }
    }
  }
  @override
  bool shouldRepaint(covariant CustomPainter old) => true;
}