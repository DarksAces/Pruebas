import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:flutter/services.dart';
import 'models/player_state.dart';
import 'screens/game_screen.dart';
import 'services/combat_engine.dart';
import 'services/localization.dart';
import 'services/iap_service.dart';
import 'services/achievement_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => PlayerState()..load()),
        ChangeNotifierProvider(create: (_) => Localization()),
        ChangeNotifierProvider(create: (_) => AchievementService()..load()),
        ChangeNotifierProxyProvider2<PlayerState, AchievementService, CombatEngine>(
          create: (ctx) => CombatEngine(ctx.read<PlayerState>(), ctx.read<AchievementService>()),
          update: (_, player, achievements, engine) => engine ?? CombatEngine(player, achievements),
        ),
        ChangeNotifierProxyProvider<PlayerState, IAPService>(
          create: (ctx) => IAPService(ctx.read<PlayerState>()),
          update: (_, player, service) => service ?? IAPService(player),
        ),
      ],
      child: MaterialApp(
        title: 'Omni Realms',
        debugShowCheckedModeBanner: false,
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
