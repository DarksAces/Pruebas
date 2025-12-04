import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'models/player_state.dart';
import 'screens/game_screen.dart';
import 'services/combat_engine.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => PlayerState()..load()),
        ChangeNotifierProxyProvider<PlayerState, CombatEngine>(
          create: (ctx) => CombatEngine(ctx.read<PlayerState>()),
          update: (_, player, engine) => engine ?? CombatEngine(player),
        ),
      ],
      child: MaterialApp(
        title: 'Space Captain',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          brightness: Brightness.dark,
          useMaterial3: true,
          textTheme: GoogleFonts.orbitronTextTheme(ThemeData.dark().textTheme),
        ),
        home: const GameScreen(),
      ),
    );
  }
}
