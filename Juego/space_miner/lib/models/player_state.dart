import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PlayerState extends ChangeNotifier {
  // Stats
  double _currentHealth = 100;
  double _maxHealth = 100;
  double _currentEnergy = 100;
  double _maxEnergy = 100;
  double _shield = 0; // Temporary shield for one turn
  
  int _level = 1;
  double _xp = 0;
  double _xpToNextLevel = 100;
  double _credits = 0;
  
  // Combat Stats
  double _attackDamage = 10;
  double _defense = 0;

  // Inventory / Equipment (Simplified for now)
  String _weaponName = "Rusty Laser Pistol";
  String _armorName = "Flight Suit";

  // Location
  String _currentWorldId = "asteroid_belt";

  // Getters
  double get currentHealth => _currentHealth;
  double get maxHealth => _maxHealth;
  double get currentEnergy => _currentEnergy;
  double get maxEnergy => _maxEnergy;
  double get shield => _shield;
  int get level => _level;
  double get xp => _xp;
  double get xpToNextLevel => _xpToNextLevel;
  double get credits => _credits;
  double get attackDamage => _attackDamage;
  String get weaponName => _weaponName;
  String get currentWorldId => _currentWorldId;

  // Actions
  void takeDamage(double amount) {
    // Shield absorbs damage first
    double damageAfterShield = (amount - _shield).clamp(0, double.infinity);
    _shield = 0; // Shield breaks after being hit (or expires next turn)
    
    double actualDamage = (damageAfterShield - _defense).clamp(0, double.infinity);
    _currentHealth = (_currentHealth - actualDamage).clamp(0, _maxHealth);
    notifyListeners();
  }

  void useEnergy(double amount) {
    _currentEnergy = (_currentEnergy - amount).clamp(0, _maxEnergy);
    notifyListeners();
  }

  void restoreEnergy(double amount) {
    _currentEnergy = (_currentEnergy + amount).clamp(0, _maxEnergy);
    notifyListeners();
  }

  void addShield(double amount) {
    _shield = amount;
    notifyListeners();
  }

  void clearShield() {
    _shield = 0;
    notifyListeners();
  }

  void heal(double amount) {
    _currentHealth = (_currentHealth + amount).clamp(0, _maxHealth);
    notifyListeners();
  }

  void gainXp(double amount) {
    _xp += amount;
    if (_xp >= _xpToNextLevel) {
      _levelUp();
    }
    notifyListeners();
  }

  void gainCredits(double amount) {
    _credits += amount;
    notifyListeners();
  }

  void equipWeapon(String name, double damage) {
    _weaponName = name;
    _attackDamage = damage;
    notifyListeners();
  }

  void travelTo(String worldId) {
    _currentWorldId = worldId;
    notifyListeners();
  }

  void _levelUp() {
    _level++;
    _xp -= _xpToNextLevel;
    _xpToNextLevel *= 1.5;
    _maxHealth += 20;
    _currentHealth = _maxHealth; // Full heal on level up
    _maxEnergy += 10;
    _currentEnergy = _maxEnergy;
    _attackDamage += 5;
    notifyListeners();
  }

  // Persistence
  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _currentHealth = prefs.getDouble('currentHealth') ?? 100;
    _maxHealth = prefs.getDouble('maxHealth') ?? 100;
    _currentEnergy = prefs.getDouble('currentEnergy') ?? 100;
    _maxEnergy = prefs.getDouble('maxEnergy') ?? 100;
    _level = prefs.getInt('level') ?? 1;
    _xp = prefs.getDouble('xp') ?? 0;
    _xpToNextLevel = prefs.getDouble('xpToNextLevel') ?? 100;
    _credits = prefs.getDouble('credits') ?? 0;
    _attackDamage = prefs.getDouble('attackDamage') ?? 10;
    _currentWorldId = prefs.getString('currentWorldId') ?? "asteroid_belt";
    notifyListeners();
  }

  Future<void> save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('currentHealth', _currentHealth);
    await prefs.setDouble('maxHealth', _maxHealth);
    await prefs.setDouble('currentEnergy', _currentEnergy);
    await prefs.setDouble('maxEnergy', _maxEnergy);
    await prefs.setInt('level', _level);
    await prefs.setDouble('xp', _xp);
    await prefs.setDouble('xpToNextLevel', _xpToNextLevel);
    await prefs.setDouble('credits', _credits);
    await prefs.setDouble('attackDamage', _attackDamage);
    await prefs.setString('currentWorldId', _currentWorldId);
  }
}
