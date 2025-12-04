import 'dart:math';
import 'world.dart';

class WorldManager {
  static final List<World> worlds = [
    World(
      id: 'asteroid_belt',
      name: 'Asteroid Belt',
      description: 'A chaotic field of drifting rocks. Home to scavengers.',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.7) {
          return Monster(
            name: 'Scavenger Drone',
            maxHealth: 30,
            attackDamage: 5,
            xpReward: 10,
            creditReward: 5,
            description: 'A rusty drone looking for scrap.',
          );
        } else {
          return Monster(
            name: 'Space Pirate',
            maxHealth: 50,
            attackDamage: 8,
            xpReward: 20,
            creditReward: 15,
            description: 'A hostile human with a laser pistol.',
          );
        }
      },
    ),
    World(
      id: 'nebula_core',
      name: 'Nebula Core',
      description: 'A swirling cloud of gas. Energy beings live here.',
      spawnPool: () {
        final rand = Random();
        if (rand.nextDouble() < 0.6) {
          return Monster(
            name: 'Plasma Wisp',
            maxHealth: 80,
            attackDamage: 12,
            xpReward: 40,
            creditReward: 25,
            description: 'A floating ball of pure energy.',
          );
        } else {
          return Monster(
            name: 'Void Beast',
            maxHealth: 150,
            attackDamage: 20,
            xpReward: 100,
            creditReward: 50,
            description: 'A terrifying creature from the dark.',
          );
        }
      },
    ),
  ];

  static World getWorld(String id) {
    return worlds.firstWhere((w) => w.id == id, orElse: () => worlds.first);
  }
}
