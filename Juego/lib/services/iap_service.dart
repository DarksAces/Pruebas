import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:in_app_purchase/in_app_purchase.dart';
import '../models/player_state.dart';

class IAPService extends ChangeNotifier {
  final InAppPurchase _iap = InAppPurchase.instance;
  late StreamSubscription<List<PurchaseDetails>> _subscription;
  final PlayerState _player;

  // Product IDs must match Google Play Console
  static const String _smallPackId = 'small_credit_pack';
  static const String _mediumPackId = 'medium_credit_pack';
  static const String _largePackId = 'large_credit_pack';

  final Set<String> _kIds = {_smallPackId, _mediumPackId, _largePackId};

  List<ProductDetails> _products = [];
  List<ProductDetails> get products => _products;

  bool _isAvailable = false;
  bool get isAvailable => _isAvailable;

  IAPService(this._player) {
    _initialize();
  }

  void _initialize() async {
    _isAvailable = await _iap.isAvailable();
    if (_isAvailable) {
      final ProductDetailsResponse response = await _iap.queryProductDetails(_kIds);
      if (response.notFoundIDs.isNotEmpty) {
        if (kDebugMode) {
          print("Products not found: ${response.notFoundIDs}");
        }
      }
      _products = response.productDetails;
      notifyListeners();
    }

    _subscription = _iap.purchaseStream.listen((purchaseDetailsList) {
      _listenToPurchaseUpdated(purchaseDetailsList);
    }, onDone: () {
      _subscription.cancel();
    }, onError: (error) {
      if (kDebugMode) {
        print("IAP Error: $error");
      }
    });
  }

  void buyProduct(String productId) {
    final ProductDetails? product = _products.firstWhere(
      (p) => p.id == productId,
      orElse: () => throw Exception("Product not found"),
    );

    if (product != null) {
      final PurchaseParam purchaseParam = PurchaseParam(productDetails: product);
      _iap.buyConsumable(purchaseParam: purchaseParam);
    }
  }

  void _listenToPurchaseUpdated(List<PurchaseDetails> purchaseDetailsList) {
    for (final PurchaseDetails purchaseDetails in purchaseDetailsList) {
      if (purchaseDetails.status == PurchaseStatus.pending) {
        // Show pending UI if needed
      } else {
        if (purchaseDetails.status == PurchaseStatus.error) {
          if (kDebugMode) {
            print("Purchase Error: ${purchaseDetails.error}");
          }
        } else if (purchaseDetails.status == PurchaseStatus.purchased ||
            purchaseDetails.status == PurchaseStatus.restored) {
          _deliverProduct(purchaseDetails);
        }
        if (purchaseDetails.pendingCompletePurchase) {
          _iap.completePurchase(purchaseDetails);
        }
      }
    }
  }

  void _deliverProduct(PurchaseDetails purchaseDetails) {
    if (purchaseDetails.productID == _smallPackId) {
      _player.gainCredits(100);
    } else if (purchaseDetails.productID == _mediumPackId) {
      _player.gainCredits(550);
    } else if (purchaseDetails.productID == _largePackId) {
      _player.gainCredits(1200);
    }
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
}
