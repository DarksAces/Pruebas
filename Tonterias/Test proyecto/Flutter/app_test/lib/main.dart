import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:lucide_icons/lucide_icons.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:geolocator/geolocator.dart' as geo;
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart'; 
import 'package:intl/intl.dart'; 

// 🔒 IMPORTS DE FIREBASE
import 'package:firebase_core/firebase_core.dart'; 
import 'package:cloud_firestore/cloud_firestore.dart';
import 'firebase_options.dart'; 
import 'api_service.dart'; 

// ==========================================
// 1. CONFIGURACIÓN Y TEMA
// ==========================================
const String MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGFuaWVsZ2FyYnJ1IiwiYSI6ImNtaWZxNmwxczA5dDAzZXIwMmsyMWgyYTkifQ.aauKhXogwH_1ZA6EDGYJCA";

class AppTheme { 
  // Colores: Azul (Primary) y Amarillo (Accent)
  static const Color primary = Color(0xFF2A4D9B); 
  static const Color accent = Color(0xFFF8C41E); 
  static const Color error = Color(0xFFE34132); 
  static const Color background = Color(0xFFF2F2F5); 
  static const Color textLight = Color(0xFFFFFFFF);
  
  static TextStyle get fontBaloo => GoogleFonts.baloo2();
  static TextStyle get fontPoppins => GoogleFonts.poppins();
}

// DATOS MOCK 
final List<Map<String, dynamic>> MOCK_STOPS = [];

// ==========================================
// 2. PROVEEDOR DE ESTADO
// ==========================================

class UserProvider extends ChangeNotifier {
  String? _nickname;

  String get nickname => _nickname ?? 'Visitante';
  bool get isAuthenticated => _nickname != null;

  void setNickname(String nick) {
    _nickname = nick;
    notifyListeners();
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 🚀 INICIALIZACIÓN DE FIREBASE
  try {
    print('🔥 Inicializando Firebase...');
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    print('✅ Firebase Core inicializado');
  } catch (e, stackTrace) {
    print("❌ Error al inicializar Firebase: $e");
    print("Stack: $stackTrace");
  }
  
  await Permission.location.request();
  
  MapboxOptions.setAccessToken(MAPBOX_ACCESS_TOKEN);
  
  // Usamos ChangeNotifierProvider para el estado del usuario
  runApp(
    ChangeNotifierProvider(
      create: (_) => UserProvider(),
      child: const MainApp(), 
    ),
  );
}

class MainApp extends StatelessWidget { 
  const MainApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Test',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(useMaterial3: true),
      home: const AuthScreen(),
    );
  }
}

// ==========================================
// 3. PANTALLA DE AUTENTICACIÓN (USUARIO/PASSWORD)
// ==========================================
class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});
  @override State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final _userController = TextEditingController(); // Usuario (se convierte en Nick)
  final _passwordController = TextEditingController(); // Contraseña (simulada)
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  void _login() async {
    final username = _userController.text.trim();
    final password = _passwordController.text.trim();
    String finalNickname;

    setState(() => _isLoading = true);

    if (username.isEmpty && password.isEmpty) {
      // 1. OPCIÓN ANÓNIMO (Si ambos campos están vacíos)
      finalNickname = 'Anónimo-${DateTime.now().millisecondsSinceEpoch % 1000}';
    } else if (username.isNotEmpty && password.isNotEmpty) {
      // 2. OPCIÓN USUARIO/PASSWORD (Simulada)
      // NOTA: Aquí iría la lógica real de Firebase Auth o un servidor.
      // Por ahora, solo usamos el username como nickname.
      finalNickname = username;
      
      // Simular un retraso para el login
      await Future.delayed(const Duration(milliseconds: 500));
      
    } else {
      // Si solo llenó uno de los dos
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('❌ Debes ingresar Usuario y Contraseña, o dejar ambos vacíos para Anónimo.'),
          backgroundColor: AppTheme.error,
        ),
      );
      setState(() => _isLoading = false);
      return;
    }

    // Éxito: Guardar el nickname (usuario o anónimo) y navegar
    if (mounted) {
      Provider.of<UserProvider>(context, listen: false).setNickname(finalNickname);
      
      Navigator.pushReplacement(
        context, 
        MaterialPageRoute(builder: (_) => MainLayout(username: finalNickname))
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.background,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Bienvenido a App Test',
                  style: AppTheme.fontBaloo.copyWith(fontSize: 28, color: AppTheme.primary),
                ),
                const SizedBox(height: 30),
                
                // Campo de Usuario
                TextFormField(
                  controller: _userController,
                  decoration: InputDecoration(
                    labelText: 'Usuario',
                    border: const OutlineInputBorder(),
                    filled: true,
                    fillColor: AppTheme.textLight,
                    prefixIcon: Icon(LucideIcons.user),
                  ),
                ),
                const SizedBox(height: 15),

                // Campo de Contraseña
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Contraseña',
                    border: const OutlineInputBorder(),
                    filled: true,
                    fillColor: AppTheme.textLight,
                    prefixIcon: Icon(LucideIcons.lock),
                  ),
                ),
                const SizedBox(height: 20),
                
                if (_isLoading)
                  const CircularProgressIndicator(color: AppTheme.accent)
                else
                  Column(
                    children: [
                      ElevatedButton.icon(
                        onPressed: _login,
                        icon: Icon(LucideIcons.logIn), // Icono de login
                        label: const Text("INICIAR SESIÓN"),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.primary,
                          foregroundColor: AppTheme.textLight,
                          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                          textStyle: AppTheme.fontPoppins.copyWith(fontWeight: FontWeight.bold),
                        ),
                      ),
                      const SizedBox(height: 10),
                      TextButton(
                        onPressed: () {
                          // Limpia campos y entra como anónimo
                          _userController.clear();
                          _passwordController.clear();
                          _login(); 
                        },
                        child: Text('Entrar como Anónimo', style: TextStyle(color: AppTheme.primary)),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class MainLayout extends StatefulWidget {
  final String username;
  const MainLayout({super.key, required this.username});
  @override State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  int _currentIndex = 0;
  // REMOVIDO: Definición de _pages fuera del build (Error de context)
  
  @override
  Widget build(BuildContext context) {
    // Definimos _pages dentro del build method para usar context
    final List<Widget> _pages = [
      const MapGameScreen(), 
      Center(
        child: Text(
          "Perfil de ${Provider.of<UserProvider>(context, listen: false).nickname}"
        )
      )
    ];

    return Scaffold(
      body: IndexedStack(index: _currentIndex, children: _pages),
      // ... (rest of the build method)
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: [
          NavigationDestination(icon: Icon(LucideIcons.map), label: "Mapa"),
          NavigationDestination(icon: Icon(LucideIcons.user), label: "Perfil"),
        ],
      ),
    );
  }
}

class MapGameScreen extends StatefulWidget {
  const MapGameScreen({super.key});
  @override State<MapGameScreen> createState() => _MapGameScreenState();
}

class _MapGameScreenState extends State<MapGameScreen> {
  // ... (Setup de Mapbox, Location, Firestore) ...
  MapboxMap? mapboxMap;
  CircleAnnotationManager? circleAnnotationManager;
  geo.Position? currentPosition;
  Map<String, dynamic>? selectedStop;
  bool isLoading = true;
  double userLat = 41.4036; 
  double userLng = 2.1874;

  bool _isSelectingLocation = false;

  List<Map<String, dynamic>> liveStops = []; 
  StreamSubscription? _firestoreSubscription; 

  @override
  void initState() {
    super.initState();
    _initLocation();
    _listenToFirestore();
  }

  @override
  void dispose() {
    _firestoreSubscription?.cancel();
    super.dispose();
  }

  void _listenToFirestore() {
    _firestoreSubscription = FirebaseFirestore.instance
        .collection('sitios')
        .snapshots()
        .listen((snapshot) {
      if (mounted) {
        final List<Map<String, dynamic>> fetchedStops = snapshot.docs.map((doc) {
          final data = doc.data();
          return {
            "id": doc.id, 
            "title": data['title'] ?? 'Sitio Anónimo',
            "lat": (data['lat'] as num).toDouble(),
            "lng": (data['lng'] as num).toDouble(),
            "author": data['author'] ?? 'Comunidad',
            "type": data['type'] ?? 'Genérico', 
            "image": data['imageUrl'] ?? data['image'] ?? 'https://images.unsplash.com/placeholder.jpg',
          };
        }).toList();

        setState(() {
          liveStops = [...MOCK_STOPS, ...fetchedStops]; 
          _drawPoints();
        });
      }
    });
  }

  _initLocation() async {
    geo.Geolocator.getPositionStream(
      locationSettings: const geo.LocationSettings(
        accuracy: geo.LocationAccuracy.high, 
        distanceFilter: 2
      )
    ).listen((pos) {
      currentPosition = pos;
      userLat = pos.latitude;
      userLng = pos.longitude;
      
      if(mounted && isLoading) {
        setState(() => isLoading = false);
        mapboxMap?.setCamera(CameraOptions(
          center: Point(coordinates: Position(pos.longitude, pos.latitude)),
          zoom: 17.0, 
          pitch: 60.0, 
          bearing: 0.0
        ));
      }
    });
  }

  _onMapCreated(MapboxMap map) async {
    mapboxMap = map;

    try { 
      await mapboxMap!.loadStyleURI("mapbox://styles/mapbox/outdoors-v12"); 
      print("✅ Estilo de mapa cargado"); 
    } catch (e) {
      print("❌ ERROR: Mapbox style load failed: $e"); 
    }

    try {
      await mapboxMap?.location.updateSettings(LocationComponentSettings(
        enabled: true,
        pulsingEnabled: false,
        puckBearingEnabled: true,
      ));
      print("✅ Avatar configurado a punto 2D predeterminado"); 
    } catch(e) {
      print("⚠️ Error al configurar ubicación: $e"); 
    }

    circleAnnotationManager = await map.annotations.createCircleAnnotationManager();
    await _drawPoints(); 

    circleAnnotationManager?.addOnCircleAnnotationClickListener(
      MyAnnotationClickListener(onTap: (annotation) {
        try {
          final stop = liveStops.firstWhere((s) => 
            (s['lat'] - annotation.geometry.coordinates.lat).abs() < 0.0001 &&
            (s['lng'] - annotation.geometry.coordinates.lng).abs() < 0.0001
          );
          setState(() => selectedStop = stop); 
        } catch (e) { 
          print("Error al encontrar parada: $e");
        }
      })
    );
  }

  _drawPoints() async {
    if (circleAnnotationManager == null) return;
    
    await circleAnnotationManager?.deleteAll();
    for (var stop in liveStops) {
      await circleAnnotationManager?.create(CircleAnnotationOptions(
        geometry: Point(coordinates: Position(stop['lng'], stop['lat'])),
        circleColor: AppTheme.error.value, // Rojo
        circleRadius: 10.0, // TAMAÑO REDUCIDO
        circleStrokeWidth: 3.0,
        circleStrokeColor: Colors.white.value,
      ));
    }
    print("✅ ${liveStops.length} puntos dibujados en el mapa");
  }

  void _confirmLocation() async {
    if (mapboxMap == null) return;

    final cameraState = await mapboxMap!.getCameraState();
    final centerPosition = cameraState.center.coordinates; 
    
    if (mounted) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => AddStopScreen(
            selectedLatitude: centerPosition.lat.toDouble(), 
            selectedLongitude: centerPosition.lng.toDouble(), 
          ), 
        ), 
      ).then((_) {
        setState(() {
          _isSelectingLocation = false;
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        MapWidget(
          key: const ValueKey("mapWidget"),
          styleUri: "mapbox://styles/mapbox/outdoors-v12",
          textureView: true, 
          cameraOptions: CameraOptions(
            center: Point(coordinates: Position(userLng, userLat)), 
            zoom: 15.0,
            pitch: 0.0
          ), 
          onMapCreated: _onMapCreated, 
        ),
        
        if (isLoading) 
          Container(
            color: Colors.black54,
            child: const Center(
              child: CircularProgressIndicator(color: AppTheme.accent)
            ),
          ),
        
        // 📌 MARCADOR CENTRAL EN MODO SELECCIÓN
        if (_isSelectingLocation)
          Center(
            child: Icon(
              LucideIcons.mapPin, 
              color: AppTheme.primary, 
              size: 50,
            ),
          ),

        // 🟢 BOTONES DE ACCIÓN (Añadir/Cancelar/Confirmar)
        Positioned(
          top: 60,
          right: 15,
          child: Column(
            children: [
              if (_isSelectingLocation)
                FloatingActionButton(
                  heroTag: 'confirm_stop_btn',
                  backgroundColor: AppTheme.primary,
                  foregroundColor: AppTheme.textLight,
                  onPressed: _confirmLocation,
                  child: Icon(LucideIcons.check),
                ),
                const SizedBox(height: 10),
              
              FloatingActionButton(
                heroTag: 'add_stop_btn',
                backgroundColor: _isSelectingLocation ? AppTheme.error : AppTheme.accent,
                foregroundColor: _isSelectingLocation ? AppTheme.textLight : AppTheme.primary,
                onPressed: () {
                  setState(() {
                    _isSelectingLocation = !_isSelectingLocation;
                    selectedStop = null; 
                  });
                },
                child: Icon(_isSelectingLocation ? LucideIcons.x : LucideIcons.plus),
              ),
            ],
          ),
        ),

        if (selectedStop != null && !_isSelectingLocation) 
          Positioned(
            bottom: 20, left: 20, right: 20,
            child: StopDetailCard(
              stop: selectedStop!, 
              onClose: () => setState(() => selectedStop = null)
            ),
          )
      ],
    );
  }
}

class MyAnnotationClickListener implements OnCircleAnnotationClickListener {
  final Function(CircleAnnotation) onTap;
  MyAnnotationClickListener({required this.onTap});
  @override
  void onCircleAnnotationClick(CircleAnnotation annotation) {
    onTap(annotation);
  }
}

// ==========================================
// 4. WIDGET DE DETALLES DEL SITIO 
// ==========================================

// ... (código anterior) ...

// ==========================================
// 4. WIDGET DE DETALLES DEL SITIO 
// ==========================================

class StopDetailCard extends StatelessWidget {
  final Map<String, dynamic> stop;
  final VoidCallback onClose;
  
  const StopDetailCard({super.key, required this.stop, required this.onClose});

  @override
  Widget build(BuildContext context) {
    // Extraemos las coordenadas
    final lat = stop['lat'].toStringAsFixed(4);
    final lng = stop['lng'].toStringAsFixed(4);

    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20)
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          
          // IMAGEN ELIMINADA: 
          // Se ha eliminado el ClipRRect que contenía CachedNetworkImage
          
          ListTile(
            title: Text(
              stop['title'], 
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20)
            ),
            // SUBTÍTULO MODIFICADO: Muestra las coordenadas
            subtitle: Text(
              // El 'type' todavía contiene el comentario inicial del creador
              'Creador: ${stop['author']}\nCoords: Lat $lat, Lng $lng', 
              style: const TextStyle(fontSize: 14, color: Colors.grey)
            ),
            isThreeLine: true, 
            trailing: IconButton(
              icon: const Icon(Icons.close), 
              onPressed: onClose
            ),
          ),
          
          // SECCIÓN: COMENTARIOS
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Divider(),
                Text(
                  'Comentario inicial: ${stop['type']}', // Muestra el comentario inicial aquí
                  style: AppTheme.fontPoppins.copyWith(
                    fontWeight: FontWeight.bold, 
                    fontSize: 14,
                    color: AppTheme.primary,
                  ),
                ),
                const SizedBox(height: 10),
                
                Text(
                  'Comentarios de la Comunidad:', 
                  style: AppTheme.fontPoppins.copyWith(
                    fontWeight: FontWeight.bold, 
                    fontSize: 16,
                    color: AppTheme.primary,
                  ),
                ),
                const SizedBox(height: 8),
                
                // StreamBuilder para escuchar comentarios en tiempo real
                CommentStream(stopId: stop['id']),
                
                // Formulario para añadir comentario
                AddCommentForm(stopId: stop['id']),
                const SizedBox(height: 10),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


// ==========================================
// 5. WIDGETS DE COMENTARIOS
// ==========================================

class CommentStream extends StatelessWidget {
  final String stopId;
  const CommentStream({super.key, required this.stopId});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot>(
      stream: FirebaseFirestore.instance
          .collection('sitios')
          .doc(stopId)
          .collection('comments')
          .orderBy('timestamp', descending: true)
          .limit(5)
          .snapshots(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator(strokeWidth: 2));
        }
        if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
          return const Text('Sé el primero en comentar.', style: TextStyle(fontStyle: FontStyle.italic));
        }

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: snapshot.data!.docs.map((doc) {
            final data = doc.data() as Map<String, dynamic>;
            final timestamp = data['timestamp'] as Timestamp?;
            final date = timestamp != null 
                ? DateFormat('dd MMM yy HH:mm').format(timestamp.toDate()) 
                : 'Fecha desconocida';

            return Padding(
              padding: const EdgeInsets.only(bottom: 8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        data['nickname'] ?? 'Anónimo', 
                        style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.error)
                      ),
                      Text(date, style: const TextStyle(fontSize: 10, color: Colors.grey)),
                    ],
                  ),
                  Text(data['text'], softWrap: true),
                ],
              ),
            );
          }).toList(),
        );
      },
    );
  }
}

class AddCommentForm extends StatefulWidget {
  final String stopId;
  const AddCommentForm({super.key, required this.stopId});
  @override State<AddCommentForm> createState() => _AddCommentFormState();
}

class _AddCommentFormState extends State<AddCommentForm> {
  final _commentController = TextEditingController();
  final ApiService apiService = ApiService();
  bool _isSending = false;

  void _submitComment(String nickname) async {
    final text = _commentController.text.trim();
    if (text.isEmpty) return;

    setState(() => _isSending = true);

    final success = await apiService.addComment(
      stopId: widget.stopId,
      nickname: nickname,
      text: text,
    );

    setState(() {
      _isSending = false;
      if (success) {
        _commentController.clear();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: const Text('Error al enviar comentario.'), backgroundColor: AppTheme.error)
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);

    return Padding(
      padding: const EdgeInsets.only(top: 10.0),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _commentController,
              decoration: InputDecoration(
                hintText: 'Comentar como ${userProvider.nickname}...',
                border: const OutlineInputBorder(),
                contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
              ),
            ),
          ),
          const SizedBox(width: 8),
          _isSending
              ? const SizedBox(
                  width: 24, 
                  height: 24, 
                  child: CircularProgressIndicator(strokeWidth: 2)
                )
              : IconButton(
                  icon: Icon(LucideIcons.send),
                  color: AppTheme.primary,
                  onPressed: () => _submitComment(userProvider.nickname),
                ),
        ],
      ),
    );
  }
}

// ==========================================
// AÑADIR SITIO SCREEN
// ==========================================
class AddStopScreen extends StatefulWidget {
  final double selectedLatitude;
  final double selectedLongitude;

  const AddStopScreen({
    super.key, 
    required this.selectedLatitude,
    required this.selectedLongitude,
  });
  
  @override 
  State<AddStopScreen> createState() => _AddStopScreenState();
}

class _AddStopScreenState extends State<AddStopScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _authorController = TextEditingController();
  final _commentController = TextEditingController(); 
  
  bool _isUploading = false;
  final apiService = ApiService(); 
  
  Future<void> _submitData() async {
    if (_formKey.currentState!.validate()) { 
      setState(() => _isUploading = true); 

      final newStop = NewStopData(
        title: _titleController.text,
        author: _authorController.text.isEmpty ? 'Anónimo' : _authorController.text,
        comment: _commentController.text.isEmpty ? null : _commentController.text,
        lat: widget.selectedLatitude,
        lng: widget.selectedLongitude,
      );

      final success = await apiService.uploadNewStop(newStop); 

      setState(() => _isUploading = false); 

      if (mounted) {
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('✅ Sitio añadido con éxito!'),
              backgroundColor: AppTheme.primary,
            ),
          );
          Navigator.pop(context); 
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text('❌ Error al subir. Revisa los logs de consola.'),
              duration: const Duration(seconds: 5),
              backgroundColor: AppTheme.error,
            ),
          );
        }
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Completa todos los campos obligatorios.')
        ),
      );
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _authorController.dispose();
    _commentController.dispose(); 
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Añadir Nuevo Sitio'),
        backgroundColor: AppTheme.primary,
        foregroundColor: AppTheme.textLight,
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Ubicación seleccionada:\nLat ${widget.selectedLatitude.toStringAsFixed(4)}, Lng ${widget.selectedLongitude.toStringAsFixed(4)}',
                style: TextStyle(
                  fontWeight: FontWeight.bold, 
                  color: AppTheme.primary
                ),
              ),
              const Divider(height: 30),

              TextFormField(
                controller: _titleController, 
                decoration: const InputDecoration(
                  labelText: 'Sitio',
                  border: OutlineInputBorder(),
                ), 
                validator: (v) => v!.isEmpty ? 'Introduce un título' : null,
              ),
              const SizedBox(height: 15),
              
              TextFormField(
                controller: _authorController, 
                decoration: const InputDecoration(
                  labelText: 'Nick Name',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 15),
              
              // CAMBIO: Campo de Comentario (opcional)
              TextFormField(
                controller: _commentController, 
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'Comentario Inicial (opcional)',
                  hintText: 'Describe por qué este sitio es interesante.',
                  border: OutlineInputBorder(),
                ), 
              ),
              const SizedBox(height: 30),

              if (_isUploading)
                const Center(
                  child: Column(
                    children: [
                      CircularProgressIndicator(color: AppTheme.accent),
                      SizedBox(height: 10),
                      Text('Subiendo metadatos...', style: TextStyle(color: AppTheme.primary)),
                    ],
                  ),
                )
              else
                ElevatedButton.icon(
                  onPressed: _submitData,
                  icon: Icon(LucideIcons.upload), 
                  label: const Text('SUBIR SITIO'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.accent, 
                    foregroundColor: AppTheme.primary, 
                    padding: const EdgeInsets.all(15),
                    textStyle: AppTheme.fontBaloo.copyWith(
                      fontSize: 18, 
                      fontWeight: FontWeight.bold
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}