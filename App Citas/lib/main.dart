
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'theme/app_theme.dart';
import 'screens/auth_screen.dart';
import 'screens/home_screen.dart';
import 'screens/questions_screen.dart';
import 'screens/profile_screen.dart';

void main() {
  runApp(const MyApp());
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

class MainNavigationWrapper extends StatefulWidget {
  const MainNavigationWrapper({super.key});

  @override
  State<MainNavigationWrapper> createState() => _MainNavigationWrapperState();
}

class _MainNavigationWrapperState extends State<MainNavigationWrapper> {
  int _currentIndex = 0;
  
  // Flag to simulate authentication state
  bool _isAuthenticated = false; 

  final List<Widget> _screens = [
    const HomeScreen(),
    const QuestionsScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    if (!_isAuthenticated) {
      // Create a temporary simplified Auth wrapper for demo
      return Scaffold(
        body: AuthScreen(), 
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            setState(() {
              _isAuthenticated = true;
            });
          },
          child: const Icon(Icons.login),
        ),
      );
    }

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
            icon: FaIcon(FontAwesomeIcons.bolt), // F3 style lightning
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
