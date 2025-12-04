import 'dart:math';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/player_state.dart';
import '../services/combat_engine.dart';
import '../services/world_manager.dart';
import '../services/localization.dart';
import 'station_screen.dart';

class GameScreen extends StatelessWidget {
  const GameScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final player = context.watch<PlayerState>();
    final combat = context.watch<CombatEngine>();
    final loc = context.watch<Localization>();
    final world = WorldManager.getWorld(player.currentWorldId);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text('${loc.get('tactical_log')}: ${world.name}', style: GoogleFonts.orbitron(color: Colors.white, fontSize: 16)),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language, color: Colors.white),
            onSelected: (String code) {
              loc.setLanguage(code);
            },
            itemBuilder: (BuildContext context) => <PopupMenuEntry<String>>[
              const PopupMenuItem<String>(value: 'en', child: Text('English')),
              const PopupMenuItem<String>(value: 'es', child: Text('Español')),
              const PopupMenuItem<String>(value: 'fr', child: Text('Français')),
              const PopupMenuItem<String>(value: 'pt', child: Text('Português')),
            ],
          ),
          IconButton(
            icon: const Icon(Icons.backpack, color: Colors.white),
            onPressed: () => _showInventory(context, player, loc),
          ),
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
                _buildStat(loc.get('hp'), '${player.currentHealth.ceil()}/${player.maxHealth.ceil()}', Colors.red),
                _buildStat(loc.get('energy'), '${player.currentEnergy.ceil()}/${player.maxEnergy.ceil()}', Colors.blueAccent),
                _buildStat(loc.get('xp'), '${player.xp.ceil()}/${player.xpToNextLevel.ceil()}', Colors.purple),
                _buildStat(loc.get('credits'), '\$${player.credits.ceil()}', Colors.green),
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
                ? _buildExplorationActions(context, world, combat, loc)
                : _buildCombatActions(context, combat, player, loc),
          ),
        ],
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
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          loc.get('you_are_in').replaceAll('%s', loc.get(world.name)),
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
              final rand = Random();
              final roll = rand.nextDouble();

              if (roll < 0.1) {
                // 10% Chance: Treasure Chest
                final creditReward = 50 + rand.nextInt(100);
                final items = ['Nano-Potion', 'Energy Cell', 'item_strength_potion', 'item_iron_skin_potion'];
                final itemKey = items[rand.nextInt(items.length)];
                
                // Give rewards
                final player = context.read<PlayerState>();
                player.gainCredits(creditReward.toDouble());
                player.addItem(itemKey);

                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    backgroundColor: Colors.grey[900],
                    title: Text(loc.get('encounter_chest_title'), style: const TextStyle(color: Colors.amber)),
                    content: Text(
                      loc.get('encounter_chest_content')
                          .replaceAll('%s', creditReward.toString())
                          .replaceFirst('%s', loc.get(itemKey)),
                      style: const TextStyle(color: Colors.white),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: Text(loc.get('action_claim'), style: const TextStyle(color: Colors.amber)),
                      ),
                    ],
                  ),
                );
              } else if (roll < 0.2) {
                // 10% Chance: Ancient Shrine
                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    backgroundColor: Colors.grey[900],
                    title: Text(loc.get('encounter_shrine_title'), style: const TextStyle(color: Colors.cyanAccent)),
                    content: Text(loc.get('encounter_shrine_content'), style: const TextStyle(color: Colors.white)),
                    actions: [
                      TextButton(
                        onPressed: () {
                          context.read<PlayerState>().heal(1000); // Full Heal
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('msg_health_restored'))));
                        },
                        child: Text(loc.get('action_pray'), style: const TextStyle(color: Colors.greenAccent)),
                      ),
                      TextButton(
                        onPressed: () {
                          context.read<PlayerState>().restoreEnergy(1000); // Full Energy
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(loc.get('msg_energy_restored'))));
                        },
                        child: Text(loc.get('action_meditate'), style: const TextStyle(color: Colors.blueAccent)),
                      ),
                    ],
                  ),
                );
              } else {
                // 80% Chance: Monster
                final monster = world.spawnPool();
                combat.startEncounter(monster, loc);
              }
            },
            icon: const Icon(Icons.radar, color: Colors.white),
            label: Text(loc.get('scan_enemies'), style: const TextStyle(color: Colors.white, fontSize: 16)),
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
              child: Text(
                "VS ${loc.get(combat.currentMonster!.name)} (HP: ${combat.currentMonster!.currentHealth.ceil()})",
                style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 16),
                overflow: TextOverflow.ellipsis,
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
}
