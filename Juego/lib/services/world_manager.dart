import 'dart:math';
import 'package:space_miner/models/world.dart';

class WorldManager {
  static final List<World> worlds = [
    World(
      id: 'kingdom_valor',
      name: 'world_kingdom_valor',
      description: 'desc_kingdom_valor',
      spawnPool: (level) { // Note: 'level' here effectively means 'floor' in our new logic if passed contextually
        // Actually, we should pass the player's floor, but the signature says 'level'.
        // Let's assume the caller passes 'Floor' here.
        int floor = level;
        double difficultyMultiplier = 1.0 + (floor * 0.1); // +10% per floor

        // Boss every 10 levels
        if (floor % 10 == 0) {
           return Monster(
            name: 'boss_orc_warlord',
            maxHealth: 400 * difficultyMultiplier, // Tougher
            attackDamage: 30 * difficultyMultiplier,
            xpReward: 300 * difficultyMultiplier,
            creditReward: 200 * difficultyMultiplier,
            description: 'desc_orc_warlord',
            isBoss: true,
          );
        }
        
        // Mini-Boss every 5 levels (that isn't a 10)
        if (floor % 5 == 0) {
           return Monster(
            name: 'enemy_dark_knight', // Re-using elite enemy as mini-boss
            maxHealth: 200 * difficultyMultiplier,
            attackDamage: 20 * difficultyMultiplier,
            xpReward: 100 * difficultyMultiplier,
            creditReward: 80 * difficultyMultiplier,
            description: 'desc_dark_knight',
            isBoss: false, // Or true if we want the warning? Let's say false for mini-boss, or add isMiniBoss
          );
        }

        final rand = Random();
        // Regular Spawns
        if (rand.nextDouble() < 0.6) {
          return Monster(
            name: 'enemy_orc_grunt',
            maxHealth: 40 * difficultyMultiplier,
            attackDamage: 8 * difficultyMultiplier,
            xpReward: 15 * difficultyMultiplier,
            creditReward: 10 * difficultyMultiplier,
            description: 'desc_orc_grunt',
          );
        } else {
          return Monster(
            name: 'enemy_dragon_whelp',
            maxHealth: 100 * difficultyMultiplier,
            attackDamage: 18 * difficultyMultiplier,
            xpReward: 50 * difficultyMultiplier,
            creditReward: 30 * difficultyMultiplier,
            description: 'desc_dragon_whelp',
          );
        }
      },
    ),
    // ... Implement similar logic for other worlds ...
    // For brevity in this edit, I will apply a generic scaler for others or reuse the logic structure
    // But since I need to replace the whole file content block, I must be explicit.
    World(
      id: 'jurassica',
      name: 'world_jurassica',
      description: 'desc_jurassica',
      spawnPool: (floor) {
        double diff = 1.5 + (floor * 0.12); // Harder base, steeper curve
        
        if (floor % 10 == 0) {
           return Monster(
            name: 'boss_t_rex_king',
            maxHealth: 800 * diff,
            attackDamage: 70 * diff,
            xpReward: 600 * diff,
            creditReward: 400 * diff,
            description: 'desc_t_rex_king',
            isBoss: true,
          );
        }

        final rand = Random();
        if (rand.nextDouble() < 0.5) {
          return Monster(
            name: 'enemy_raptor_pack',
            maxHealth: 60 * diff,
            attackDamage: 14 * diff,
            xpReward: 25 * diff,
            creditReward: 20 * diff,
            description: 'desc_raptor_pack',
          );
        } else {
          return Monster(
            name: 'enemy_triceratops',
            maxHealth: 180 * diff,
            attackDamage: 12 * diff,
            xpReward: 50 * diff,
            creditReward: 35 * diff,
            description: 'desc_triceratops',
          );
        }
      },
    ),
    World(
      id: 'neon_tokyo',
      name: 'world_neon_tokyo',
      description: 'desc_neon_tokyo',
      spawnPool: (floor) {
        double diff = 2.0 + (floor * 0.15); 

        if (floor % 10 == 0) {
           return Monster(
            name: 'boss_mecha_shogun',
            maxHealth: 1000 * diff,
            attackDamage: 100 * diff,
            xpReward: 800 * diff,
            creditReward: 600 * diff,
            description: 'desc_mecha_shogun',
            isBoss: true,
          );
        }

        final rand = Random();
        if (rand.nextDouble() < 0.6) {
          return Monster(
            name: 'enemy_yakuza_bot',
            maxHealth: 120 * diff,
            attackDamage: 25 * diff,
            xpReward: 60 * diff,
            creditReward: 50 * diff,
            description: 'desc_yakuza_bot',
          );
        } else {
          return Monster(
            name: 'enemy_cyber_ninja',
            maxHealth: 90 * diff,
            attackDamage: 40 * diff,
            xpReward: 80 * diff,
            creditReward: 70 * diff,
            description: 'desc_cyber_ninja',
          );
        }
      },
    ),
    World(
      id: 'mystic_woods',
      name: 'world_mystic_woods',
      description: 'desc_mystic_woods',
      spawnPool: (floor) {
        double diff = 3.0 + (floor * 0.18); 

        if (floor % 10 == 0) {
           return Monster(
            name: 'boss_elder_ent',
            maxHealth: 1500 * diff,
            attackDamage: 120 * diff,
            xpReward: 1000 * diff,
            creditReward: 800 * diff,
            description: 'desc_elder_ent',
            isBoss: true,
          );
        }

        final rand = Random();
        if (rand.nextDouble() < 0.5) {
          return Monster(
            name: 'enemy_goblin_thief',
            maxHealth: 50 * diff,
            attackDamage: 15 * diff,
            xpReward: 40 * diff,
            creditReward: 30 * diff,
            description: 'desc_goblin_thief',
          );
        } else {
          return Monster(
            name: 'enemy_ent_guardian',
            maxHealth: 300 * diff,
            attackDamage: 25 * diff,
            xpReward: 90 * diff,
            creditReward: 50 * diff,
            description: 'desc_ent_guardian',
          );
        }
      },
    ),
    World(
      id: 'void_nexus',
      name: 'world_void_nexus',
      description: 'desc_void_nexus',
      spawnPool: (floor) {
        double diff = 5.0 + (floor * 0.25); // Extreme scaling
        return Monster(
          name: 'enemy_void_stalker',
          maxHealth: 200 * diff,
          attackDamage: 80 * diff,
          xpReward: 300 * diff,
          creditReward: 200 * diff,
          description: 'desc_void_stalker',
        );
      },
    ),
  ];

  static World getWorld(String id) {
    return worlds.firstWhere((w) => w.id == id, orElse: () => worlds.first);
  }
}
