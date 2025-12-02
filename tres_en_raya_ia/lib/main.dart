import 'package:flutter/material.dart';
import 'package:flutter/services.dart'; // Necesario para el Portapapeles
import 'dart:math';
import 'dart:convert';

void main() {
  runApp(const SuperTresEnRayaApp());
}

class SuperTresEnRayaApp extends StatelessWidget {
  const SuperTresEnRayaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Súper Tres en Raya ML',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.indigo,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF1A1A2E),
        sliderTheme: const SliderThemeData(
          showValueIndicator: ShowValueIndicator.always,
        ),
      ),
      home: const MenuPrincipal(),
    );
  }
}

// --- CEREBRO Q-LEARNING (INTELIGENCIA ARTIFICIAL) ---
class CerebroIA {
  Map<String, List<double>> qTable = {};
  double learningRate = 0.5; 
  double discountFactor = 0.9;
  double explorationRate = 1.0; 
  
  final Random _rng = Random();

  String _generarClaveEstado(List<String> tablero) {
    return tablero.map((e) => e == '' ? '-' : e).join();
  }

  int obtenerMejorMovimiento(List<String> tablero, {bool modoJuegoReal = false}) {
    String estado = _generarClaveEstado(tablero);
    
    if (!qTable.containsKey(estado)) {
      qTable[estado] = List.generate(9, (index) => _rng.nextDouble() * 0.1);
    }

    double umbralExploracion = modoJuegoReal ? 0.02 : explorationRate;

    if (_rng.nextDouble() < umbralExploracion) {
      List<int> vacios = [];
      for (int i = 0; i < 9; i++) if (tablero[i] == '') vacios.add(i);
      if (vacios.isEmpty) return -1;
      return vacios[_rng.nextInt(vacios.length)];
    } else {
      List<double> valores = qTable[estado]!;
      double maxVal = -99999.0;
      int bestMove = -1;
      
      List<int> mejoresMovimientos = [];
      
      for (int i = 0; i < 9; i++) {
        if (tablero[i] == '') {
          if (valores[i] > maxVal) {
            maxVal = valores[i];
            mejoresMovimientos = [i];
          } else if (valores[i] == maxVal) {
            mejoresMovimientos.add(i);
          }
        }
      }
      
      if (mejoresMovimientos.isEmpty) {
         List<int> vacios = [];
         for (int i = 0; i < 9; i++) if (tablero[i] == '') vacios.add(i);
         return vacios.isNotEmpty ? vacios.first : -1;
      }
      return mejoresMovimientos[_rng.nextInt(mejoresMovimientos.length)];
    }
  }

  void aprender(List<String> estadoActual, int accion, double recompensa, List<String> estadoSiguiente) {
    String stateKey = _generarClaveEstado(estadoActual);
    String nextStateKey = _generarClaveEstado(estadoSiguiente);

    if (!qTable.containsKey(stateKey)) qTable[stateKey] = List.filled(9, 0.0);
    if (!qTable.containsKey(nextStateKey)) qTable[nextStateKey] = List.filled(9, 0.0);

    double qActual = qTable[stateKey]![accion];
    double maxQFuturo = (recompensa.abs() > 5.0) ? 0.0 : qTable[nextStateKey]!.reduce(max);

    double nuevoQ = qActual + learningRate * (recompensa + discountFactor * maxQFuturo - qActual);
    qTable[stateKey]![accion] = nuevoQ;
  }

  // --- Lógica de Oponente Inteligente para Entrenamiento ---
  int _movimientoOponenteInteligente(List<String> tablero, String jugador) {
    String rival = (jugador == 'X') ? 'O' : 'X';
    
    // 1. Intentar Ganar
    for (int i = 0; i < 9; i++) {
      if (tablero[i] == '') {
        tablero[i] = jugador;
        if (_checkWin(tablero, jugador)) {
          tablero[i] = ''; 
          return i;
        }
        tablero[i] = '';
      }
    }
    
    // 2. Bloquear al Rival
    for (int i = 0; i < 9; i++) {
      if (tablero[i] == '') {
        tablero[i] = rival; 
        if (_checkWin(tablero, rival)) {
          tablero[i] = '';
          return i; 
        }
        tablero[i] = '';
      }
    }

    // 3. Jugar Aleatorio si no hay peligro
    List<int> vacios = [];
    for (int i = 0; i < 9; i++) if (tablero[i] == '') vacios.add(i);
    if (vacios.isEmpty) return -1;
    return vacios[_rng.nextInt(vacios.length)];
  }

  Future<void> entrenamientoIntensivo(int episodios, Function(double) onProgress) async {
    explorationRate = 1.0;
    learningRate = 0.2; 
    
    for (int i = 0; i < episodios; i++) {
      List<String> tablero = List.filled(9, '');
      bool juegoTerminado = false;
      List<Map<String, dynamic>> historial = [];

      if (explorationRate > 0.1) explorationRate -= (0.9 / episodios);

      while (!juegoTerminado) {
        int moveX;
        if (_rng.nextDouble() < 0.7) {
           moveX = _movimientoOponenteInteligente(tablero, 'X');
        } else {
           List<int> vacios = [];
           for (int k = 0; k < 9; k++) if (tablero[k] == '') vacios.add(k);
           if (vacios.isEmpty) break;
           moveX = vacios[_rng.nextInt(vacios.length)];
        }
        
        if (moveX == -1) break; 
        tablero[moveX] = 'X'; 

        if (_checkWin(tablero, 'X') || !tablero.contains('')) {
           _aplicarBackpropagation(historial, -10.0);
           juegoTerminado = true;
           break;
        }

        int moveO = obtenerMejorMovimiento(tablero);
        if (moveO == -1) break;

        List<String> estadoAntes = List<String>.from(tablero); 
        tablero[moveO] = 'O';
        
        historial.add({
          'estado': estadoAntes,
          'accion': moveO,
          'siguiente': List<String>.from(tablero)
        });

        if (_checkWin(tablero, 'O')) {
          _aplicarBackpropagation(historial, 10.0);
          juegoTerminado = true;
        } else if (!tablero.contains('')) {
          _aplicarBackpropagation(historial, 2.0); 
          juegoTerminado = true;
        }
      }
      if (i % 50 == 0) { 
        onProgress(i / episodios);
        await Future.delayed(Duration.zero);
      }
    }
    explorationRate = 0.0;
    learningRate = 0.5; 
  }

  void _aplicarBackpropagation(List<Map<String, dynamic>> historial, double recompensaFinal) {
    double recompensaAcumulada = recompensaFinal;
    for (int i = historial.length - 1; i >= 0; i--) {
      var paso = historial[i];
      List<String> estado = List<String>.from(paso['estado']);
      List<String> siguiente = List<String>.from(paso['siguiente']);
      aprender(estado, paso['accion'], recompensaAcumulada, siguiente);
      recompensaAcumulada *= discountFactor;
    }
  }

  bool _checkWin(List<String> board, String player) {
    List<List<int>> wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    for(var w in wins) {
      if(board[w[0]] == player && board[w[1]] == player && board[w[2]] == player) return true;
    }
    return false;
  }
}

CerebroIA cerebroGlobal = CerebroIA();

// --- MENÚ PRINCIPAL ---
class MenuPrincipal extends StatefulWidget {
  const MenuPrincipal({super.key});
  @override
  State<MenuPrincipal> createState() => _MenuPrincipalState();
}

class _MenuPrincipalState extends State<MenuPrincipal> {
  double progresoEntrenamiento = 0.0;
  bool entrenando = false;
  int estadosAprendidos = 0;

  void _entrenarIA() async {
    setState(() { entrenando = true; progresoEntrenamiento = 0.0; });
    await cerebroGlobal.entrenamientoIntensivo(10000, (progreso) {
      setState(() => progresoEntrenamiento = progreso);
    });
    setState(() { entrenando = false; estadosAprendidos = cerebroGlobal.qTable.length; });
  }

  void _exportarCerebro() async {
    String jsonCerebro = jsonEncode(cerebroGlobal.qTable);
    
    // 1. Imprimir en consola (por si acaso)
    print(jsonCerebro);

    // 2. Copiar al Portapapeles del móvil
    await Clipboard.setData(ClipboardData(text: jsonCerebro));
    
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('✅ ¡Cerebro copiado! Pégalo en tus Notas/WhatsApp'),
        backgroundColor: Colors.green,
        duration: Duration(seconds: 4),
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.psychology, size: 80, color: Color(0xFFE94560)),
              const SizedBox(height: 20),
              const Text("TRES EN RAYA\nIA vs IA", textAlign: TextAlign.center, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 30),
              
              // PANEL DE ENTRENAMIENTO
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(20), border: Border.all(color: Colors.white24)),
                child: Column(
                  children: [
                    const Text("1. Entrenar Cerebro (Invisible)", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 10),
                    if (entrenando) LinearProgressIndicator(value: progresoEntrenamiento, color: const Color(0xFFE94560)),
                    Text("Sabiduría: $estadosAprendidos situaciones", style: const TextStyle(color: Colors.white70)),
                    const SizedBox(height: 10),
                    ElevatedButton.icon(
                      onPressed: entrenando ? null : _entrenarIA, 
                      icon: const Icon(Icons.flash_on), 
                      label: const Text("Entrenamiento Maestro (10k)")
                    ),
                    const SizedBox(height: 10),
                    // BOTÓN DE EXPORTAR MEJORADO
                    if (estadosAprendidos > 0)
                      OutlinedButton.icon(
                        onPressed: _exportarCerebro,
                        icon: const Icon(Icons.copy, color: Colors.greenAccent),
                        label: const Text("Copiar Datos Aprendidos", style: TextStyle(color: Colors.greenAccent)),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: Colors.greenAccent),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              
              // JUGAR
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const TableroJuego(modoEspectador: false))),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF4ECCA3), padding: const EdgeInsets.all(15)),
                  child: const Text("2. JUGAR (Tú vs IA)", style: TextStyle(fontSize: 18, color: Colors.black)),
                ),
              ),
              const SizedBox(height: 15),

              // NUEVO: COLISEO
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const TableroJuego(modoEspectador: true))),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFE94560), padding: const EdgeInsets.all(15)),
                  child: const Text("3. VER COLISEO (IA vs IA)", style: TextStyle(fontSize: 18, color: Colors.white)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// --- PANTALLA DE JUEGO (VERSATIL) ---
class TableroJuego extends StatefulWidget {
  final bool modoEspectador;
  const TableroJuego({super.key, required this.modoEspectador});

  @override
  State<TableroJuego> createState() => _TableroJuegoState();
}

class _TableroJuegoState extends State<TableroJuego> {
  List<String> tablero = List.filled(9, '');
  bool esTurnoDeX = true;
  String resultado = '';
  List<Map<String, dynamic>> historialPartidaIA = [];

  @override
  void initState() {
    super.initState();
    if (widget.modoEspectador) {
      Future.delayed(const Duration(seconds: 1), _bucleEspectador);
    }
  }

  void _bucleEspectador() async {
    if (!mounted) return;
    
    if (resultado != '') {
      await Future.delayed(const Duration(seconds: 2));
      if (mounted) _reiniciar();
      await Future.delayed(const Duration(seconds: 1));
    }

    if (resultado == '') {
      if (esTurnoDeX) {
        _movimientoAleatorioX();
      } else {
        _movimientoIA();
      }
      if (mounted) Future.delayed(const Duration(milliseconds: 600), _bucleEspectador);
    } else {
      if (mounted) _bucleEspectador();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.modoEspectador ? 'Coliseo de IAs' : 'Tú vs IA'), 
        backgroundColor: Colors.transparent, 
        elevation: 0
      ),
      body: Column(
        children: [
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(20),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, crossAxisSpacing: 10, mainAxisSpacing: 10),
              itemCount: 9,
              itemBuilder: (context, index) {
                return GestureDetector(
                  onTap: widget.modoEspectador ? null : () => _movimientoHumano(index),
                  child: Container(
                    decoration: BoxDecoration(color: const Color(0xFF16213E), borderRadius: BorderRadius.circular(10)),
                    child: Center(
                      child: Text(tablero[index], style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: tablero[index] == 'X' ? const Color(0xFFE94560) : const Color(0xFF4ECCA3))),
                    ),
                  ),
                );
              },
            ),
          ),
          if (resultado != '') 
            Container(
              padding: const EdgeInsets.all(15),
              color: Colors.black45,
              child: Text(resultado, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
            ),
          const SizedBox(height: 20),
          if (!widget.modoEspectador)
             ElevatedButton(onPressed: _reiniciar, child: const Text("Nueva Partida")),
          if (widget.modoEspectador)
             const Text("Observando batalla automática...", style: TextStyle(color: Colors.grey)),
          const SizedBox(height: 40),
        ],
      ),
    );
  }

  void _reiniciar() {
    setState(() {
      tablero = List.filled(9, '');
      resultado = '';
      esTurnoDeX = true;
      historialPartidaIA.clear();
    });
  }

  // --- LÓGICA DE MOVIMIENTOS ---

  void _movimientoHumano(int index) {
    if (tablero[index] != '' || resultado != '') return;
    setState(() {
      tablero[index] = 'X';
      esTurnoDeX = false;
    });
    if (_checkFinal('X')) return;
    Future.delayed(const Duration(milliseconds: 300), _movimientoIA);
  }

  void _movimientoAleatorioX() {
    List<int> vacios = [];
    for (int i = 0; i < 9; i++) if (tablero[i] == '') vacios.add(i);
    if (vacios.isEmpty) return;
    
    int move = vacios[Random().nextInt(vacios.length)];
    setState(() {
      tablero[move] = 'X';
      esTurnoDeX = false;
    });
    _checkFinal('X');
  }

  void _movimientoIA() {
    List<String> estadoAntes = List<String>.from(tablero); 
    int move = cerebroGlobal.obtenerMejorMovimiento(tablero, modoJuegoReal: true);
    
    if (move != -1) {
      setState(() {
        tablero[move] = 'O';
        esTurnoDeX = true;
        historialPartidaIA.add({
          'estado': estadoAntes,
          'accion': move,
          'siguiente': List<String>.from(tablero) 
        });
      });
      _checkFinal('O');
    }
  }

  bool _checkFinal(String ultimoJugador) {
    bool haGanado = false;
    List<List<int>> wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    
    for(var w in wins) {
      if(tablero[w[0]] != '' && tablero[w[0]] == tablero[w[1]] && tablero[w[1]] == tablero[w[2]]) haGanado = true;
    }

    if (haGanado) {
      setState(() => resultado = "$ultimoJugador Gana!");
      double recompensa = (ultimoJugador == 'O') ? 20.0 : -20.0;
      cerebroGlobal._aplicarBackpropagation(historialPartidaIA, recompensa);
      return true;
    } else if (!tablero.contains('')) {
      setState(() => resultado = "Empate");
      cerebroGlobal._aplicarBackpropagation(historialPartidaIA, 5.0);
      return true;
    }
    return false;
  }
}