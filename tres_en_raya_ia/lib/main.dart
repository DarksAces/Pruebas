import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math';
import 'dart:convert';
import 'dart:html' as html; // Necesario para descargas en Web

void main() {
  runApp(const Conecta4App());
}

class Conecta4App extends StatelessWidget {
  const Conecta4App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Conecta 4 ML Pro',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.indigo,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF0D1117),
        // Eliminamos dialogTheme global para evitar conflictos de tipos en DDC
      ),
      home: const MenuPrincipal(),
    );
  }
}

// --- CEREBRO HÍBRIDO (Q-LEARNING + HEURÍSTICA TÁCTICA) ---
class CerebroIA {
  Map<String, List<double>> qTable = {};
  double learningRate = 0.2; // Aprendizaje agresivo
  double discountFactor = 0.9;
  double explorationRate = 0.0; // Ya no exploramos tanto en juego real
  
  final Random _rng = Random();
  static const int ROWS = 6;
  static const int COLS = 7;

  String _generarClaveEstado(List<List<int>> tablero) {
    return tablero.expand((row) => row).join();
  }

  // --- INTELIGENCIA MEJORADA ---
  int obtenerMejorColumna(List<List<int>> tablero, {bool modoJuegoReal = false}) {
    List<int> validas = _getColumnasValidas(tablero);
    if (validas.isEmpty) return -1;

    // NIVEL 1: INSTINTO ASESINO (Si puedo ganar, gano)
    for (int col in validas) {
      if (_simularYVerificar(tablero, col, 2)) return col;
    }

    // NIVEL 2: SUPERVIVENCIA (Si el humano va a ganar, bloqueo)
    // Solo aplicamos esto rigurosamente en modo juego real para que parezca lista
    if (modoJuegoReal) {
      for (int col in validas) {
        if (_simularYVerificar(tablero, col, 1)) return col; // Bloquear al J1
      }
    }

    // NIVEL 3: CEREBRO Q-LEARNING + ESTRATEGIA CENTRAL
    String estado = _generarClaveEstado(tablero);
    if (!qTable.containsKey(estado)) {
      // Si no sabe nada, prefiere el centro (columnas 3, 2, 4...)
      validas.sort((a, b) => (3 - a).abs().compareTo((3 - b).abs()));
      return validas.first;
    }

    // Usar Q-Table
    if (modoJuegoReal || _rng.nextDouble() > explorationRate) {
      List<double> valores = qTable[estado]!;
      double maxVal = -99999.0;
      List<int> mejores = [];
      
      for (int col in validas) {
        // Añadimos un pequeño sesgo hacia el centro para romper empates
        double sesgoCentro = (3.0 - (3 - col).abs()) * 0.01;
        double val = valores[col] + sesgoCentro;
        
        if (val > maxVal) {
          maxVal = val;
          mejores = [col];
        } else if ((val - maxVal).abs() < 0.001) {
          mejores.add(col);
        }
      }
      return mejores[_rng.nextInt(mejores.length)];
    } else {
      return validas[_rng.nextInt(validas.length)];
    }
  }

  // Simula poner una ficha y ve si gana alguien
  bool _simularYVerificar(List<List<int>> tablero, int col, int jugador) {
    int row = -1;
    // Encontrar donde cae
    for (int r = ROWS - 1; r >= 0; r--) {
      if (tablero[r][col] == 0) {
        row = r;
        break;
      }
    }
    if (row == -1) return false;

    // Colocar temporalmente
    tablero[row][col] = jugador;
    bool gana = checkWin(tablero, jugador);
    tablero[row][col] = 0; // Quitar (Backtrack)
    return gana;
  }

  List<int> _getColumnasValidas(List<List<int>> tablero) {
    List<int> validas = [];
    for (int c = 0; c < COLS; c++) {
      if (tablero[0][c] == 0) validas.add(c);
    }
    return validas;
  }

  void aprender(List<List<int>> estadoActual, int col, double recompensa, List<List<int>> estadoSiguiente) {
    String key = _generarClaveEstado(estadoActual);
    String nextKey = _generarClaveEstado(estadoSiguiente);

    if (!qTable.containsKey(key)) qTable[key] = List.filled(COLS, 0.0);
    if (!qTable.containsKey(nextKey)) qTable[nextKey] = List.filled(COLS, 0.0);

    double qActual = qTable[key]![col];
    double maxQFuturo = 0.0;
    
    // Solo miramos el futuro si no es terminal
    if (recompensa.abs() < 10.0) {
       List<int> validas = _getColumnasValidas(estadoSiguiente);
       if (validas.isNotEmpty) {
         maxQFuturo = validas.map((c) => qTable[nextKey]![c]).reduce(max);
       }
    }

    qTable[key]![col] = qActual + learningRate * (recompensa + discountFactor * maxQFuturo - qActual);
  }

  // --- ENTRENAMIENTO AUTOMÁTICO ---
  Future<void> entrenamientoIntensivo(int episodios, Function(double) onProgress, {bool refinar = false}) async {
    if (!refinar) explorationRate = 1.0; 
    
    for (int i = 0; i < episodios; i++) {
      List<List<int>> tablero = List.generate(ROWS, (_) => List.filled(COLS, 0));
      bool fin = false;
      List<Map<String, dynamic>> historial = [];
      
      // Decae la exploración
      if (explorationRate > 0.1) explorationRate *= 0.9995;

      while (!fin) {
        // --- Turno Rival (Inteligente) ---
        int moveRival = -1;
        List<int> validas = _getColumnasValidas(tablero);
        if (validas.isEmpty) break;

        for (int c in validas) if (_simularYVerificar(tablero, c, 1)) moveRival = c;
        if (moveRival == -1) {
           for (int c in validas) if (_simularYVerificar(tablero, c, 2)) moveRival = c;
        }
        if (moveRival == -1) moveRival = validas[_rng.nextInt(validas.length)];

        tablero = _aplicarMovimiento(tablero, moveRival, 1);

        if (checkWin(tablero, 1)) {
          _backprop(historial, -20.0); 
          fin = true; break;
        }
        if (_getColumnasValidas(tablero).isEmpty) {
           _backprop(historial, 5.0); 
           fin = true; break;
        }

        // --- Turno IA ---
        int moveIA = obtenerMejorColumna(tablero); 
        if (moveIA == -1) break;

        var estadoAntes = List.generate(ROWS, (idx) => List<int>.from(tablero[idx]));
        tablero = _aplicarMovimiento(tablero, moveIA, 2);
        
        historial.add({
          'estado': estadoAntes,
          'col': moveIA,
          'siguiente': List.generate(ROWS, (idx) => List<int>.from(tablero[idx]))
        });

        if (checkWin(tablero, 2)) {
          _backprop(historial, 50.0); 
          fin = true;
        }
      }
      
      if (i % 100 == 0) {
        onProgress(i / episodios);
        await Future.delayed(Duration.zero);
      }
    }
    if (!refinar) explorationRate = 0.0; 
  }

  List<List<int>> _aplicarMovimiento(List<List<int>> tablero, int col, int jugador) {
    for (int r = ROWS - 1; r >= 0; r--) {
      if (tablero[r][col] == 0) {
        tablero[r][col] = jugador;
        return tablero;
      }
    }
    return tablero;
  }

  void _backprop(List<Map<String, dynamic>> historial, double recompensa) {
    double r = recompensa;
    for (int i = historial.length - 1; i >= 0; i--) {
      aprender(historial[i]['estado'], historial[i]['col'], r, historial[i]['siguiente']);
      r *= 0.8; 
    }
  }

  bool checkWin(List<List<int>> b, int p) {
    for (int r = 0; r < ROWS; r++)
      for (int c = 0; c < COLS - 3; c++)
        if (b[r][c] == p && b[r][c+1] == p && b[r][c+2] == p && b[r][c+3] == p) return true;
    for (int r = 0; r < ROWS - 3; r++)
      for (int c = 0; c < COLS; c++)
        if (b[r][c] == p && b[r+1][c] == p && b[r+2][c] == p && b[r+3][c] == p) return true;
    for (int r = 3; r < ROWS; r++)
      for (int c = 0; c < COLS - 3; c++)
        if (b[r][c] == p && b[r-1][c+1] == p && b[r-2][c+2] == p && b[r-3][c+3] == p) return true;
    for (int r = 0; r < ROWS - 3; r++)
      for (int c = 0; c < COLS - 3; c++)
        if (b[r][c] == p && b[r+1][c+1] == p && b[r+2][c+2] == p && b[r+3][c+3] == p) return true;
    return false;
  }
  
  void modoJuegoSerio() => explorationRate = 0.0;
}

CerebroIA cerebroGlobal = CerebroIA();

// --- MENÚ PRINCIPAL ---
class MenuPrincipal extends StatefulWidget {
  const MenuPrincipal({super.key});
  @override
  State<MenuPrincipal> createState() => _MenuPrincipalState();
}

class _MenuPrincipalState extends State<MenuPrincipal> {
  double progreso = 0.0;
  bool entrenando = false;
  bool _afkActivo = false;
  int estados = 0;

  void _entrenarBasico() async {
    setState(() { entrenando = true; _afkActivo = false; progreso = 0.0; });
    await cerebroGlobal.entrenamientoIntensivo(3000, (p) => setState(() => progreso = p));
    setState(() { entrenando = false; estados = cerebroGlobal.qTable.length; });
  }

  void _toggleAFK() async {
    if (_afkActivo) {
      setState(() => _afkActivo = false);
      return;
    }

    setState(() { _afkActivo = true; entrenando = true; });
    
    while (_afkActivo) {
      await cerebroGlobal.entrenamientoIntensivo(500, (p) {}, refinar: true);
      setState(() { estados = cerebroGlobal.qTable.length; });
      await Future.delayed(const Duration(milliseconds: 50));
    }

    setState(() { entrenando = false; progreso = 0.0; });
    cerebroGlobal.modoJuegoSerio(); 
  }

  // FUNCIÓN DE DESCARGA (NUEVA)
  void _descargarCerebro() {
    // Convertimos el mapa a JSON
    final jsonStr = jsonEncode(cerebroGlobal.qTable);
    
    // Creamos un Blob con los datos (tipo archivo virtual)
    final bytes = utf8.encode(jsonStr);
    final blob = html.Blob([bytes], 'application/json');
    
    // Creamos una URL para ese Blob
    final url = html.Url.createObjectUrlFromBlob(blob);
    
    // Creamos un elemento <a> invisible, le asignamos la URL y lo clicamos
    final anchor = html.AnchorElement(href: url)
      ..setAttribute("download", "cerebro_conecta4_${estados}_estados.json")
      ..click();
      
    // Limpiamos
    html.Url.revokeObjectUrl(url);
    
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Descarga iniciada...'), backgroundColor: Colors.green)
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.grid_4x4, size: 80, color: Colors.cyanAccent),
            const SizedBox(height: 20),
            const Text("CONECTA 4 MASTER", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 40),
            
            if (entrenando && !_afkActivo) 
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 10),
                child: LinearProgressIndicator(value: progreso, color: Colors.cyanAccent),
              ),
            
            if (_afkActivo)
              const Padding(
                padding: EdgeInsets.all(10.0),
                child: Text("⚡ ENTRENAMIENTO AFK ACTIVO ⚡", style: TextStyle(color: Colors.yellow, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
              ),

            Text("Sabiduría IA: $estados nodos", style: const TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),
            
            ElevatedButton(
              onPressed: entrenando ? null : _entrenarBasico,
              style: ElevatedButton.styleFrom(backgroundColor: Colors.blueGrey),
              child: const Text("1. Entrenar Rápido (3k)"),
            ),
            const SizedBox(height: 10),
            
            ElevatedButton.icon(
              onPressed: (entrenando && !_afkActivo) ? null : _toggleAFK,
              icon: Icon(_afkActivo ? Icons.stop : Icons.loop),
              style: ElevatedButton.styleFrom(
                backgroundColor: _afkActivo ? Colors.redAccent : Colors.purpleAccent,
                foregroundColor: Colors.white
              ),
              label: Text(_afkActivo ? "DETENER AFK" : "2. ENTRENAMIENTO AFK (Infinito)"),
            ),
            
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: entrenando ? null : () => Navigator.push(context, MaterialPageRoute(builder: (_) => const TableroJuego())),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan, padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15)),
              child: const Text("3. JUGAR AHORA", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
            ),
            
             const SizedBox(height: 10),
             // Botón cambiado de Copiar a Descargar
             TextButton.icon(
               onPressed: (estados > 0) ? _descargarCerebro : null,
               icon: const Icon(Icons.download, size: 18),
               label: const Text("Descargar Cerebro (.json)", style: TextStyle(color: Colors.white30)),
             )
          ],
        ),
      ),
    );
  }
}

// --- TABLERO DE JUEGO ---
class TableroJuego extends StatefulWidget {
  const TableroJuego({super.key});
  @override
  State<TableroJuego> createState() => _TableroJuegoState();
}

class _TableroJuegoState extends State<TableroJuego> {
  List<List<int>> tablero = List.generate(6, (_) => List.filled(7, 0));
  bool turnoHumano = true;
  bool bloqueado = false;

  void _jugar(int col) async {
    if (bloqueado) return;
    
    // Humano
    if (!_colocarFicha(col, 1)) return; 
    if (_verificarFin(1)) return;

    setState(() { bloqueado = true; });
    await Future.delayed(const Duration(milliseconds: 600));

    // IA
    int colIA = cerebroGlobal.obtenerMejorColumna(tablero, modoJuegoReal: true);
    if (colIA != -1) {
      _colocarFicha(colIA, 2);
      _verificarFin(2);
    }
    setState(() { bloqueado = false; });
  }

  bool _colocarFicha(int col, int jugador) {
    for (int r = 5; r >= 0; r--) {
      if (tablero[r][col] == 0) {
        setState(() => tablero[r][col] = jugador);
        return true;
      }
    }
    return false;
  }

  bool _verificarFin(int jugador) {
    if (cerebroGlobal.checkWin(tablero, jugador)) {
      String titulo = jugador == 1 ? "¡VICTORIA!" : "IA GANA";
      Color colorTitulo = jugador == 1 ? Colors.greenAccent : Colors.redAccent;
      
      // Diálogo con estilo local para evitar problemas de Theme
      showDialog(
        context: context, 
        barrierDismissible: false,
        builder: (_) => AlertDialog(
          backgroundColor: const Color(0xFF2D333B),
          title: Text(titulo, textAlign: TextAlign.center, style: TextStyle(color: colorTitulo, fontSize: 28, fontWeight: FontWeight.bold)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.emoji_events, size: 50, color: Colors.amber),
              const SizedBox(height: 10),
              Text(jugador == 1 ? "¡Has vencido a la máquina!" : "La IA ha dominado esta ronda.", textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70)),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () { Navigator.pop(context); _reiniciar(); },
              child: const Text("JUGAR OTRA VEZ", style: TextStyle(color: Colors.cyanAccent))
            )
          ],
        )
      );
      return true;
    }
    // Empate
    if (cerebroGlobal._getColumnasValidas(tablero).isEmpty) {
       showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => AlertDialog(
          backgroundColor: const Color(0xFF2D333B),
          title: const Text("EMPATE", textAlign: TextAlign.center, style: TextStyle(color: Colors.white)),
          content: const Text("Tablero lleno. Nadie gana.", textAlign: TextAlign.center, style: TextStyle(color: Colors.white70)),
          actions: [
            TextButton(onPressed: () { Navigator.pop(context); _reiniciar(); }, child: const Text("REINICIAR"))
          ]
        )
      );
      return true;
    }
    return false;
  }

  void _reiniciar() {
    setState(() {
      tablero = List.generate(6, (_) => List.filled(7, 0));
      bloqueado = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Humano (Rojo) vs IA (Amarillo)"), backgroundColor: Colors.transparent, elevation: 0),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.blue[900],
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 10, offset: Offset(5,5))]
                ),
                padding: const EdgeInsets.all(8),
                child: Column(
                  children: List.generate(6, (row) => Expanded(
                    child: Row(
                      children: List.generate(7, (col) => Expanded(
                        child: GestureDetector(
                          onTap: () => _jugar(col),
                          child: Container(
                            margin: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: _getColor(tablero[row][col]),
                              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 2, offset: Offset(1,1))] // Sombra interior simulada
                            ),
                          ),
                        ),
                      )),
                    ),
                  )),
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Text("Toca una columna para jugar", style: TextStyle(color: Colors.white54))
          ],
        ),
      ),
    );
  }

  Color _getColor(int val) {
    if (val == 1) return Colors.redAccent;
    if (val == 2) return Colors.yellowAccent;
    return const Color(0xFF0A0E14);
  }
}