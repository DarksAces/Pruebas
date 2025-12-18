
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'theme/app_theme.dart';
import 'screens/auth_screen.dart';
import 'screens/home_screen.dart';
import 'screens/questions_screen.dart';
import 'screens/matches_screen.dart'; // Added import
import 'screens/profile_screen.dart';

import 'services/database_service.dart';
import 'services/auth_service.dart';
import 'services/purchase_service.dart'; // Added PurchaseService import
import 'package:firebase_core/firebase_core.dart'; 
import 'package:firebase_auth/firebase_auth.dart'; // Ensure FirebaseAuth is imported
import 'models/models.dart' as app_models; // Alias to avoid conflict if any
import 'package:provider/provider.dart';
import 'firebase_options.dart'; // User needs this

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // We try to initialize, but it might fail if user handles config manually or hasn't created file
  try {
     await Firebase.initializeApp(
       options: DefaultFirebaseOptions.currentPlatform,
     );
  } catch (e) {
    print('Firebase initialization failed (Expected if config not done): $e');
  }
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => PurchaseService()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Citas',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme, 
      themeMode: ThemeMode.system,
      home: const MainNavigationWrapper(),
    );
  }
}

class MainNavigationWrapper extends StatelessWidget {
  const MainNavigationWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: AuthService().authStateChanges,
      builder: (context, snapshot) {
         if (snapshot.connectionState == ConnectionState.active) {
            final User? user = snapshot.data;
            if (user == null) {
              return const AuthScreen(); // Not authenticated
            }
            
            // Check Verification
            if (!user.emailVerified) {
              return const VerificationScreen();
            }

            // Save User Data to Firestore (Side effect)
            // Ideally this should be done in a Controller or Service specific method,
            // but for simplicity we can trigger it here or in AppScaffold init.
            _saveUserData(user);

             return const AppScaffold(); // Authenticated & Verified
         }
         return const Scaffold(body: Center(child: CircularProgressIndicator()));
      },
    );
  }

  void _saveUserData(User user) {
    // Save minimal data from Google Auth
    final appUser = app_models.User(
      id: user.uid,
      name: user.displayName ?? 'New User',
      age: 0, // Placeholder
      bio: 'No bio yet.',
      imageUrl: user.photoURL ?? 'https://via.placeholder.com/150',
      photos: [],
    );
    DatabaseService().ensureUserExists(appUser);
  }
}

class VerificationScreen extends StatelessWidget {
  const VerificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
     return Scaffold(
       body: Center(
         child: Column(
           mainAxisAlignment: MainAxisAlignment.center,
           children: [
             const Icon(Icons.mail_lock, size: 80, color: Colors.orange),
             const SizedBox(height: 20),
             const Text('Please verify your email'),
             const SizedBox(height: 20),
             ElevatedButton(
               onPressed: () async {
                 await AuthService().sendEmailVerification();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Verification email sent!')),
                  );
               },
               child: const Text('Send Verification Email'),
             ),
             TextButton(
               onPressed: () async {
                 await AuthService().reloadUser();
               },
               child: const Text('I have verified'),
             ),
              TextButton(
               onPressed: () async {
                 await AuthService().signOut();
               },
               child: const Text('Sign Out'),
             ),
           ],
         ),
       ),
     );
  }
}

class AppScaffold extends StatefulWidget {
  const AppScaffold({super.key});

  @override
  State<AppScaffold> createState() => _AppScaffoldState();
}

class _AppScaffoldState extends State<AppScaffold> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeScreen(),
    const MatchesScreen(), // Added MatchesScreen
    const QuestionsScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: FaIcon(FontAwesomeIcons.fire),
            label: 'Discover',
          ),
          NavigationDestination(
            icon: FaIcon(FontAwesomeIcons.solidHeart), // Icon for Matches
            label: 'Matches',
          ),
          NavigationDestination(
            icon: FaIcon(FontAwesomeIcons.bolt),
            label: 'Questions',
          ),
          NavigationDestination(
            icon: FaIcon(FontAwesomeIcons.user),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
