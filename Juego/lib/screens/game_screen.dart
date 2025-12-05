import 'dart:math';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/player_state.dart';
import '../services/combat_engine.dart';
import '../services/world_manager.dart';
import '../services/localization.dart';
import 'station_screen.dart';

import '../services/achievement_service.dart';

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  @override
  void initState() {
    super.initState();
    // Listen for achievements
    final achievements = context.read<AchievementService>();
    achievements.addListener(_onAchievementUnlocked);
  }

  @override
  void dispose() {
    context.read<AchievementService>().removeListener(_onAchievementUnlocked);
    super.dispose();
  }

  void _onAchievementUnlocked() {
    final achievements = context.read<AchievementService>();
    if (achievements.recentlyUnlocked.isNotEmpty) {
      for (final achievement in achievements.recentlyUnlocked) {
         ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: Colors.amber,
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("🏆 ACHIEVEMENT UNLOCKED!", style: GoogleFonts.orbitron(fontWeight: FontWeight.bold, color: Colors.black)),
                Text(achievement.title, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black)),
                Text(achievement.description, style: const TextStyle(color: Colors.black87)),
              ],
            ),
            duration: const Duration(seconds: 4),
          ),
        );
      }
      achievements.clearRecentlyUnlocked();
    }
  }

  @override
  @override
  Widget build(BuildContext context) {
    final player = context.watch<PlayerState>();
    final combat = context.watch<CombatEngine>();
    final loc = context.watch<Localization>();
    final world = WorldManager.getWorld(player.currentWorldId);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.black, Colors.blueGrey[900]!],
          ),
        ),
        child: SafeArea( // Use SafeArea
          child: Column(
            children: [
              // Custom AppBar
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                color: Colors.black54,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                         Text(loc.get(world.name), style: GoogleFonts.orbitron(color: Colors.white, fontSize: 16)),
                         Text(loc.get('floor_label').replaceFirst('%s', player.currentFloor.toString()), style: GoogleFonts.orbitron(color: Colors.cyanAccent, fontSize: 14, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    Row(
                      children: [
                        IconButton(
                          icon: const Icon(Icons.backpack, color: Colors.white),
                          onPressed: () => _showInventory(context, player, loc),
                        ),
                        IconButton(
                          icon: const Icon(Icons.emoji_events, color: Colors.amber),
                          onPressed: () => _showAchievements(context),
                        ),
                        PopupMenuButton<String>(
                          icon: const Icon(Icons.language, color: Colors.cyanAccent),
                          onSelected: (String code) {
                             loc.setLanguage(code);
                          },
                          itemBuilder: (BuildContext context) => <PopupMenuEntry<String>>[
                            const PopupMenuItem<String>(value: 'en', child: Text('English')),
                            const PopupMenuItem<String>(value: 'es', child: Text('Español')),
                            const PopupMenuItem<String>(value: 'fr', child: Text('Français')),
                          ],
                        ),
                      ],
                    )
                  ],
                ),
              ),
              
              // Top Stats Bar
              Container(
                margin: const EdgeInsets.all(8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.6),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white10),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildStat(loc.get('hp'), '${player.currentHealth.ceil()}/${player.maxHealth.ceil()}', Colors.red),
                    _buildStat(loc.get('energy'), '${player.currentEnergy.ceil()}/${player.maxEnergy.ceil()}', Colors.blueAccent),
                    _buildStat(loc.get('xp'), 'Lvl ${player.level}', Colors.purple), // Compact XP
                    _buildStat(loc.get('credits'), '\$${player.credits.ceil()}', Colors.green),
                  ],
                ),
              ),

              // Combat Log (The "Game")
              Expanded(
                child: Container(
                  width: double.infinity,
                  margin: const EdgeInsets.symmetric(horizontal: 8),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.greenAccent.withOpacity(0.1)),
                  ),
                  child: ListView.builder(
                    reverse: true, // Newest at bottom
                    itemCount: combat.combatLog.length,
                    itemBuilder: (context, index) {
                      // Reverse index for display
                      final logIndex = combat.combatLog.length - 1 - index;
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2.0),
                        child: Text(
                          combat.combatLog[logIndex],
                          style: GoogleFonts.firaCode(
                            color: Colors.greenAccent, 
                            fontSize: 13,
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),

              // Action Area
              Container(
                height: 260, 
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.black87,
                  borderRadius: const BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20)),
                  boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 10, offset: const Offset(0, -5))],
                ),
                child: combat.currentMonster == null
                    ? _buildExplorationActions(context, world, combat, loc)
                    : _buildCombatActions(context, combat, player, loc),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showInventory(BuildContext context, PlayerState player, Localization loc) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.grey[900],
      builder: (ctx) {
        return Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text(loc.get('inventory'), style: GoogleFonts.orbitron(color: Colors.white, fontSize: 20)),
              const SizedBox(height: 20),
              if (player.inventory.isEmpty)
                Text(loc.get('empty_inventory'), style: const TextStyle(color: Colors.white70)),
              Expanded(
                child: ListView.builder(
                  itemCount: player.inventory.length,
                  itemBuilder: (ctx, index) {
                    final itemId = player.inventory[index];
                    return ListTile(
                      title: Text(itemId, style: const TextStyle(color: Colors.white)),
                      trailing: ElevatedButton(
                        onPressed: () {
                          _useItem(context, player, itemId);
                          Navigator.pop(context);
                        },
                        child: Text(loc.get('use')),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _useItem(BuildContext context, PlayerState player, String itemId) {
    final loc = context.read<Localization>();
    if (itemId == 'Nano-Potion') {
      player.heal(50);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Used Nano-Potion: +50 HP")));
    } else if (itemId == 'Phoenix Chip') {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Phoenix Chip is passive (auto-revive).")));
    } else if (itemId == 'Energy Cell') {
      player.restoreEnergy(50);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Used Energy Cell: +50 Energy")));
    } else if (itemId == 'Overcharge Chip') {
      player.enableDamageBoost();
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Overcharge Chip Active! +50% Dmg next fight.")));
    } else if (itemId == 'Hyper-Shield') {
      player.enableShieldBoost();
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Hyper-Shield Active! Start next fight w/ 100 Shield.")));
    } else if (itemId == 'Mega-Potion') {
      player.heal(150);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Used Mega-Potion: +150 HP")));
    } else if (itemId == 'Nano-Elixir') {
      player.restoreEnergy(100);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Used Nano-Elixir: +100 Energy")));
    } else if (itemId == 'Titanium Plating') {
      player.upgradeMaxHealth(20);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Titanium Plating Installed: +20 Max HP")));
    } else if (itemId == 'Neural Link') {
      player.upgradeMaxEnergy(10);
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Neural Link Connected: +10 Max Energy")));
    } else if (itemId == 'item_strength_potion' || itemId == 'Strength Potion') {
      player.enableDamageBoost();
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('msg_used_strength'))));
    } else if (itemId == 'item_iron_skin_potion' || itemId == 'Iron Skin Potion') {
      player.enableDefenseBoost();
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('msg_used_iron_skin'))));
    } else if (itemId == 'item_luck_charm' || itemId == 'Luck Charm') {
      player.enableLuckBoost();
      player.removeItem(itemId);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('msg_used_luck'))));
    }
  }

  Widget _buildStat(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        Text(value, style: const TextStyle(color: Colors.white)),
      ],
    );
  }

  Widget _buildExplorationActions(BuildContext context, dynamic world, CombatEngine combat, Localization loc) {
    final player = context.read<PlayerState>();
    int maxFloor = player.getMaxFloorForWorld(player.currentWorldId);

    // Calculate checkpoints
    List<int> checkpoints = [];
    for (int i = 10; i <= maxFloor; i+=10) {
      checkpoints.add(i);
    }
    // Always add floor 1 if not present and we want to allow going back? 
    // Usually roguelikes are forward only or town. 
    // User said "teleport to level 10 when you complete it".
    
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (checkpoints.isNotEmpty)
          Padding(
             padding: const EdgeInsets.only(bottom: 10),
             child: SizedBox(
              height: 40,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: [
                   const Center(child: Text("Portal: ", style: TextStyle(color: Colors.cyanAccent))),
                   ...checkpoints.map((floor) => Padding(
                     padding: const EdgeInsets.symmetric(horizontal: 4.0),
                     child: ActionChip(
                       label: Text("F$floor"),
                       backgroundColor: Colors.cyan.withOpacity(0.2),
                       onPressed: () {
                          player.teleportToFloor(floor);
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Warped to Floor $floor")));
                       },
                     ),
                   )),
                ],
              ),
             ),
          ),

        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange[900],
              padding: const EdgeInsets.all(16),
              elevation: 5,
            ),
            onPressed: () {
               // Exploration Logic
               final rand = Random();
               final roll = rand.nextDouble();
               
               if (roll < 0.1) {
                  // Healing Spring
                  context.read<PlayerState>().heal(50);
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('healing_spring'))));
               } else {
                  final monster = world.spawnPool(player.currentFloor);
                  combat.startEncounter(monster, loc);
               }
            },
            icon: const Icon(Icons.explore, color: Colors.white),
            label: Text(loc.get('explore_floor').replaceFirst('%s', player.currentFloor.toString()), style: GoogleFonts.orbitron(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
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
            label: Text(loc.get('dock_station'), style: const TextStyle(color: Colors.amber, fontSize: 16)),
          ),
        ),
      ],
    );
  }

  Widget _buildCombatActions(BuildContext context, CombatEngine combat, PlayerState player, Localization loc) {
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
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                   if (combat.currentMonster!.isBoss)
                    Text("⚠️ BOSS BATTLE ⚠️", style: GoogleFonts.orbitron(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 18)),
                  Text(
                    "VS ${loc.get(combat.currentMonster!.name)} (HP: ${combat.currentMonster!.currentHealth.ceil()})",
                    style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 16),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
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
            Expanded(child: _buildSkillButton(context, combat, player, loc.get('blaster'), 0, Colors.redAccent, "Blaster")),
            const SizedBox(width: 8),
            Expanded(child: _buildSkillButton(context, combat, player, loc.get('plasma_cannon'), 30, Colors.orangeAccent, "Plasma Cannon")),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(child: _buildSkillButton(context, combat, player, loc.get('shield'), 15, Colors.blueAccent, "Shield")),
            const SizedBox(width: 8),
            Expanded(child: _buildSkillButton(context, combat, player, loc.get('repair'), 20, Colors.greenAccent, "Repair")),
          ],
        ),
        const SizedBox(height: 8),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.purple[900]),
            onPressed: () => combat.useSkill("Recharge"),
            child: Text("${loc.get('recharge')} (+40 ${loc.get('energy')})", style: const TextStyle(color: Colors.white)),
          ),
        ),
      ],
    );
  }

  Widget _buildSkillButton(BuildContext context, CombatEngine combat, PlayerState player, String label, double cost, Color color, String skillId) {
    final canAfford = player.currentEnergy >= cost;
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: canAfford ? color.withOpacity(0.2) : Colors.grey[800],
        side: BorderSide(color: canAfford ? color : Colors.grey),
        padding: const EdgeInsets.symmetric(vertical: 12),
      ),
      onPressed: canAfford ? () => combat.useSkill(skillId) : null,
      child: Column(
        children: [
          Text(label, style: TextStyle(color: canAfford ? Colors.white : Colors.white38, fontWeight: FontWeight.bold)),
          Text("${cost.toInt()} Energy", style: TextStyle(color: canAfford ? Colors.white70 : Colors.white24, fontSize: 10)),
        ],
      ),
    );
  }

  void _showAchievements(BuildContext context) {
    final achievements = context.read<AchievementService>();
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.grey[900],
      builder: (ctx) {
        return Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text("Achievements", style: GoogleFonts.orbitron(color: Colors.amber, fontSize: 20)),
              const SizedBox(height: 20),
              Expanded(
                child: ListView.builder(
                  itemCount: achievements.achievements.length,
                  itemBuilder: (ctx, index) {
                    final achievement = achievements.achievements[index];
                    final isUnlocked = achievement.isUnlocked;
                    
                    if (achievement.hidden && !isUnlocked) {
                      return const ListTile(
                        leading: Icon(Icons.lock, color: Colors.grey),
                        title: Text("???", style: TextStyle(color: Colors.grey)),
                        subtitle: Text("Hidden Achievement", style: TextStyle(color: Colors.grey)),
                      );
                    }

                    return ListTile(
                      leading: Icon(
                        isUnlocked ? Icons.emoji_events : Icons.lock_outline, 
                        color: isUnlocked ? Colors.amber : Colors.grey
                      ),
                      title: Text(achievement.title, style: TextStyle(color: isUnlocked ? Colors.white : Colors.grey)),
                      subtitle: Text(achievement.description, style: TextStyle(color: isUnlocked ? Colors.white70 : Colors.grey)),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
