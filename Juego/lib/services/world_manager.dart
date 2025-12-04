import 'dart:math';
import 'package:space_miner/models/world.dart';

class WorldManager {
  static final List<World> worlds = [
    World(
      id: 'kingdom_valor',
      name: 'world_kingdom_valor',
      description: 'desc_kingdom_valor',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.6) {
          return Monster(
            name: 'enemy_orc_grunt',
            maxHealth: 40,
            attackDamage: 8,
            xpReward: 15,
            creditReward: 10,
            description: 'desc_orc_grunt',
          );
        } else if (rand.nextDouble() < 0.9) {
          return Monster(
            name: 'enemy_dark_knight',
            maxHealth: 80,
            attackDamage: 15,
            xpReward: 35,
            creditReward: 25,
            description: 'desc_dark_knight',
          );
        } else {
          return Monster(
            name: 'enemy_dragon_whelp',
            maxHealth: 120,
            attackDamage: 25,
            xpReward: 60,
            creditReward: 50,
            description: 'desc_dragon_whelp',
          );
        }
      },
    ),
    World(
      id: 'jurassica',
      name: 'world_jurassica',
      description: 'desc_jurassica',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.5) {
          return Monster(
            name: 'enemy_raptor_pack',
            maxHealth: 50,
            attackDamage: 12,
            xpReward: 20,
            creditReward: 15,
            description: 'desc_raptor_pack',
          );
        } else if (rand.nextDouble() < 0.8) {
          return Monster(
            name: 'enemy_triceratops',
            maxHealth: 150,
            attackDamage: 10,
            xpReward: 45,
            creditReward: 30,
            description: 'desc_triceratops',
          );
        } else {
          return Monster(
            name: 'enemy_t_rex',
            maxHealth: 250,
            attackDamage: 40,
            xpReward: 100,
            creditReward: 80,
            description: 'desc_t_rex',
          );
        }
      },
    ),
    World(
      id: 'neon_tokyo',
      name: 'world_neon_tokyo',
      description: 'desc_neon_tokyo',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.6) {
          return Monster(
            name: 'enemy_yakuza_bot',
            maxHealth: 100,
            attackDamage: 20,
            xpReward: 50,
            creditReward: 40,
            description: 'desc_yakuza_bot',
          );
        } else {
          return Monster(
            name: 'enemy_cyber_ninja',
            maxHealth: 80,
            attackDamage: 35,
            xpReward: 70,
            creditReward: 60,
            description: 'desc_cyber_ninja',
          );
        }
      },
    ),
    World(
      id: 'mystic_woods',
      name: 'world_mystic_woods',
      description: 'desc_mystic_woods',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.5) {
          return Monster(
            name: 'enemy_goblin_thief',
            maxHealth: 30,
            attackDamage: 5,
            xpReward: 10,
            creditReward: 5,
            description: 'desc_goblin_thief',
          );
        } else if (rand.nextDouble() < 0.8) {
          return Monster(
            name: 'enemy_ent_guardian',
            maxHealth: 200,
            attackDamage: 15,
            xpReward: 60,
            creditReward: 20,
            description: 'desc_ent_guardian',
          );
        } else {
          return Monster(
            name: 'enemy_spirit_wolf',
            maxHealth: 90,
            attackDamage: 22,
            xpReward: 40,
            creditReward: 15,
            description: 'desc_spirit_wolf',
          );
        }
      },
    ),
    World(
      id: 'void_nexus',
      name: 'world_void_nexus',
      description: 'desc_void_nexus',
      spawnPool: () {
        return Monster(
          name: 'enemy_void_stalker',
          maxHealth: 100,
          attackDamage: 60,
          xpReward: 200,
          creditReward: 100,
          description: 'desc_void_stalker',
        );
      },
    ),
  ];

  static World getWorld(String id) {
    return worlds.firstWhere((w) => w.id == id, orElse: () => worlds.first);
  }
}
