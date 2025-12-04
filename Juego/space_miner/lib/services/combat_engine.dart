import 'dart:math';
import 'package:flutter/foundation.dart';
import '../models/player_state.dart';
import '../models/world.dart';

enum EnemyIntent { attack, charge, defend }

class CombatEngine extends ChangeNotifier {
  final PlayerState _player;
  Monster? _currentMonster;
  final List<String> _combatLog = [];
  bool _isPlayerTurn = true;
  EnemyIntent _nextEnemyMove = EnemyIntent.attack;

  CombatEngine(this._player);

  Monster? get currentMonster => _currentMonster;
  List<String> get combatLog => _combatLog;
  bool get isPlayerTurn => _isPlayerTurn;
  EnemyIntent get nextEnemyMove => _nextEnemyMove;

  void startEncounter(Monster monster) {
    _currentMonster = monster;
    _isPlayerTurn = true;
    _combatLog.clear();
    _player.clearShield(); // Reset shield
    _determineEnemyIntent(); // Decide first move
    _log("⚠️ Encountered a ${monster.name}!");
    _log(monster.description);
    notifyListeners();
  }

  void useSkill(String skillName) {
    if (_currentMonster == null || !_isPlayerTurn) return;

    bool actionTaken = false;

    switch (skillName) {
      case 'Blaster':
        if (_player.currentEnergy >= 0) { // Free
           double damage = _player.attackDamage;
           _dealDamageToEnemy(damage);
           _log("🔫 Blaster shot for ${damage.toInt()} damage.");
           actionTaken = true;
        }
        break;
      case 'Plasma Cannon':
        if (_player.currentEnergy >= 30) {
          _player.useEnergy(30);
          double damage = _player.attackDamage * 2.5;
          _dealDamageToEnemy(damage);
          _log("💥 Plasma Cannon hit for ${damage.toInt()} damage!");
          actionTaken = true;
        } else {
          _log("❌ Not enough Energy!");
        }
        break;
      case 'Shield':
        if (_player.currentEnergy >= 15) {
          _player.useEnergy(15);
          _player.addShield(50); // Block 50 damage
          _log("🛡️ Shields raised! Blocking next attack.");
          actionTaken = true;
        } else {
          _log("❌ Not enough Energy!");
        }
        break;
      case 'Recharge':
        _player.restoreEnergy(40);
        _log("⚡ Recharging systems... +40 Energy.");
        actionTaken = true;
        break;
      case 'Repair':
        if (_player.currentEnergy >= 20) {
          _player.useEnergy(20);
          _player.heal(30);
          _log("🔧 Nanobots repaired 30 HP.");
          actionTaken = true;
        } else {
          _log("❌ Not enough Energy!");
        }
        break;
    }

    if (actionTaken) {
      if (_currentMonster != null && _currentMonster!.isDead) {
        _victory();
      } else {
        _endPlayerTurn();
      }
    }
  }

  void _dealDamageToEnemy(double damage) {
    if (_currentMonster == null) return;
    _currentMonster!.currentHealth -= damage;
  }

  void playerFlee() {
    if (!_isPlayerTurn) return;
    _log("💨 You escaped safely.");
    _currentMonster = null;
    notifyListeners();
  }

  void _endPlayerTurn() {
    _isPlayerTurn = false;
    notifyListeners();
    
    Future.delayed(const Duration(seconds: 1), () {
      if (_currentMonster != null && !_currentMonster!.isDead) {
        _enemyTurn();
      }
    });
  }

  bool _enemyCharged = false;

  void _determineEnemyIntent() {
    if (_enemyCharged) {
      _nextEnemyMove = EnemyIntent.attack; // Forced heavy attack
      return;
    }

    final rand = Random();
    double roll = rand.nextDouble();
    
    if (roll < 0.6) {
      _nextEnemyMove = EnemyIntent.attack;
    } else if (roll < 0.85) {
      _nextEnemyMove = EnemyIntent.charge;
    } else {
      _nextEnemyMove = EnemyIntent.defend;
    }
  }

  void _enemyTurn() {
    if (_currentMonster == null) return;

    // Execute the move we planned last turn
    switch (_nextEnemyMove) {
      case EnemyIntent.attack:
        double damage = _currentMonster!.attackDamage;
        if (_enemyCharged) {
          damage *= 3; // Massive damage
          _log("🔥 SUPER ATTACK! ${_currentMonster!.name} hits for ${damage.toInt()}!");
          _enemyCharged = false;
        } else {
          _log("⚔️ ${_currentMonster!.name} attacks for ${damage.toInt()} damage.");
        }
        _player.takeDamage(damage);
        break;
      case EnemyIntent.charge:
        _log("⚠️ ${_currentMonster!.name} is charging energy! Watch out!");
        _enemyCharged = true;
        break;
      case EnemyIntent.defend:
        _log("🛡️ ${_currentMonster!.name} is observing you.");
        break;
    }

    if (_player.currentHealth <= 0) {
      _defeat();
    } else {
      _isPlayerTurn = true;
      // Plan next move
      _determineEnemyIntent();
      notifyListeners();
    }
  }


  void _victory() {
    if (_currentMonster == null) return;
    _log("🏆 You defeated ${_currentMonster!.name}!");
    _log("💰 Gained \$${_currentMonster!.creditReward} and ${_currentMonster!.xpReward} XP.");
    
    _player.gainCredits(_currentMonster!.creditReward);
    _player.gainXp(_currentMonster!.xpReward);
    _player.save(); // Save progress after fight

    _currentMonster = null;
    notifyListeners();
  }

  void _defeat() {
    _log("💀 You were defeated...");
    _log("Resurrecting at base...");
    _player.heal(_player.maxHealth); // Full heal
    _currentMonster = null;
    notifyListeners();
  }

  void _log(String message) {
    _combatLog.add(message);
    // Keep log size manageable
    if (_combatLog.length > 50) {
      _combatLog.removeAt(0);
    }
    notifyListeners();
  }
}
