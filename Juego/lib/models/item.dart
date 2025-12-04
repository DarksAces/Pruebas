enum ItemType { heal, revive }

class Item {
  final String id;
  final String name;
  final String description;
  final ItemType type;
  final double value; // Heal amount or other value

  Item({
    required this.id,
    required this.name,
    required this.description,
    required this.type,
    required this.value,
  });
}
