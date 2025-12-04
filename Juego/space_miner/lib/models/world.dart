class Monster {
  final String name;
  final double maxHealth;
  double currentHealth;
  final double attackDamage;
  final double xpReward;
  final double creditReward;
  final String description;

  Monster({
    required this.name,
    required this.maxHealth,
    required this.attackDamage,
    required this.xpReward,
    required this.creditReward,
    required this.description,
  }) : currentHealth = maxHealth;

  bool get isDead => currentHealth <= 0;
}

class World {
  final String id;
  final String name;
  final String description;
  final List<Monster> Function() spawnPool; // Returns a new instance of a monster

  World({
    required this.id,
    required this.name,
    required this.description,
    required this.spawnPool,
  });
}
