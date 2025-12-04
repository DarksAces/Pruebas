import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/player_state.dart';
import '../services/combat_engine.dart';
import '../services/world_manager.dart';
import 'station_screen.dart';

class GameScreen extends StatelessWidget {
  const GameScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final player = context.watch<PlayerState>();
    final combat = context.watch<CombatEngine>();
    final world = WorldManager.getWorld(player.currentWorldId);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text('Tactical Log: ${world.name} (v2.0)', style: GoogleFonts.orbitron(color: Colors.white, fontSize: 16)),
        actions: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Center(child: Text('Lvl ${player.level}', style: const TextStyle(color: Colors.amber))),
          )
        ],
      ),
      body: Column(
        children: [
          // Top Stats Bar
          Container(
            padding: const EdgeInsets.all(12),
            color: Colors.grey[900],
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildStat('HP', '${player.currentHealth.ceil()}/${player.maxHealth.ceil()}', Colors.red),
                _buildStat('ENERGY', '${player.currentEnergy.ceil()}/${player.maxEnergy.ceil()}', Colors.blueAccent),
                _buildStat('XP', '${player.xp.ceil()}/${player.xpToNextLevel.ceil()}', Colors.purple),
                _buildStat('Credits', '\$${player.credits.ceil()}', Colors.green),
              ],
            ),
          ),

          // Combat Log (The "Game")
          Expanded(
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                border: Border.symmetric(horizontal: BorderSide(color: Colors.greenAccent.withOpacity(0.3))),
              ),
              child: ListView.builder(
                reverse: true, // Newest at bottom
                itemCount: combat.combatLog.length,
                itemBuilder: (context, index) {
                  // Reverse index for display
                  final logIndex = combat.combatLog.length - 1 - index;
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: Text(
                      combat.combatLog[logIndex],
                      style: GoogleFonts.firaCode(
                        color: Colors.greenAccent, 
                        fontSize: 14,
                      ),
                    ),
                  );
                },
              ),
            ),
          ),

          // Action Area
          Container(
            height: 280, // Taller for skills
            padding: const EdgeInsets.all(16),
            color: Colors.grey[900],
            child: combat.currentMonster == null
                ? _buildExplorationActions(context, world, combat)
                : _buildCombatActions(context, combat, player),
          ),
        ],
      ),
    );
  }

  Widget _buildStat(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        Text(value, style: const TextStyle(color: Colors.white)),
      ],
    );
  }

  Widget _buildExplorationActions(BuildContext context, dynamic world, CombatEngine combat) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          "You are in ${world.name}.",
          style: const TextStyle(color: Colors.white70, fontStyle: FontStyle.italic),
        ),
        const SizedBox(height: 20),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue[900],
              padding: const EdgeInsets.all(16),
            ),
            onPressed: () {
              final monster = world.spawnPool();
              combat.startEncounter(monster);
            },
            icon: const Icon(Icons.radar, color: Colors.white),
            label: const Text("SCAN FOR ENEMIES", style: TextStyle(color: Colors.white, fontSize: 16)),
          ),
        ),
        const SizedBox(height: 10),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.all(16),
              side: const BorderSide(color: Colors.amber),
            ),
            onPressed: () {
              showModalBottomSheet(
                context: context,
                builder: (_) => const StationScreen(),
              );
            },
            icon: const Icon(Icons.store, color: Colors.amber),
            label: const Text("DOCK AT STATION", style: TextStyle(color: Colors.amber, fontSize: 16)),
          ),
        ),
      ],
    );
  }

  Widget _buildCombatActions(BuildContext context, CombatEngine combat, PlayerState player) {
    if (!combat.isPlayerTurn) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(color: Colors.red),
            const SizedBox(height: 10),
            Text("Enemy Turn...", style: GoogleFonts.orbitron(color: Colors.redAccent, fontSize: 18)),
          ],
        ),
      );
    }

    // Enemy Intent Indicator
    IconData intentIcon;
    Color intentColor;
    String intentText;
    
    switch (combat.nextEnemyMove) {
      case EnemyIntent.attack:
        intentIcon = Icons.flash_on;
        intentColor = Colors.red;
        intentText = "Attacking";
        break;
      case EnemyIntent.charge:
        intentIcon = Icons.warning;
        intentColor = Colors.orange;
        intentText = "Charging!";
        break;
      case EnemyIntent.defend:
        intentIcon = Icons.shield;
        intentColor = Colors.blue;
        intentText = "Defending";
        break;
    }

    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text("VS ${combat.currentMonster!.name} (HP: ${combat.currentMonster!.currentHealth.ceil()})",
                style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 16)),
            Row(
              children: [
                Text("Intent: $intentText ", style: TextStyle(color: intentColor)),
                Icon(intentIcon, color: intentColor),
              ],
            ),
          ],
        ),
        const Divider(color: Colors.white24),
        const Spacer(),
        
        // Skill Grid
        Row(
          children: [
            Expanded(child: _buildSkillButton(context, combat, player, "Blaster", 0, Colors.redAccent)),
            const SizedBox(width: 8),
            Expanded(child: _buildSkillButton(context, combat, player, "Plasma Cannon", 30, Colors.orangeAccent)),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(child: _buildSkillButton(context, combat, player, "Shield", 15, Colors.blueAccent)),
            const SizedBox(width: 8),
            Expanded(child: _buildSkillButton(context, combat, player, "Repair", 20, Colors.greenAccent)),
          ],
        ),
        const SizedBox(height: 8),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.purple[900]),
            onPressed: () => combat.useSkill("Recharge"),
            child: const Text("RECHARGE (+40 Energy)", style: TextStyle(color: Colors.white)),
          ),
        ),
      ],
    );
  }

  Widget _buildSkillButton(BuildContext context, CombatEngine combat, PlayerState player, String name, double cost, Color color) {
    final canAfford = player.currentEnergy >= cost;
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: canAfford ? color.withOpacity(0.2) : Colors.grey[800],
        side: BorderSide(color: canAfford ? color : Colors.grey),
        padding: const EdgeInsets.symmetric(vertical: 12),
      ),
      onPressed: canAfford ? () => combat.useSkill(name) : null,
      child: Column(
        children: [
          Text(name, style: TextStyle(color: canAfford ? Colors.white : Colors.white38, fontWeight: FontWeight.bold)),
          Text("${cost.toInt()} Energy", style: TextStyle(color: canAfford ? Colors.white70 : Colors.white24, fontSize: 10)),
        ],
      ),
    );
  }
}
