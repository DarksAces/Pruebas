
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

class PurchaseService extends ChangeNotifier {
  static final PurchaseService _instance = PurchaseService._internal();
  factory PurchaseService() => _instance;
  PurchaseService._internal();

  final InAppPurchase _iap = InAppPurchase.instance;
  late StreamSubscription<List<PurchaseDetails>> _subscription;

  List<ProductDetails> _products = [];
  List<ProductDetails> get products => _products;

  bool _isAvailable = false;
  bool get isAvailable => _isAvailable;

  bool _isPremium = false;
  bool get isPremium => _isPremium;

  // Define your Product IDs from Play Console / App Store
  static const Set<String> _kIds = <String>{
    'premium_monthly',
    'premium_yearly',
  };

  void initialize() {
    final Stream<List<PurchaseDetails>> purchaseUpdated = _iap.purchaseStream;
    _subscription = purchaseUpdated.listen((purchaseDetailsList) {
      _listenToPurchaseUpdated(purchaseDetailsList);
    }, onDone: () {
      _subscription.cancel();
    }, onError: (error) {
      if (kDebugMode) {
        print('IAP Error: $error');
      }
    });
    
    _initStoreInfo();
  }

  Future<void> _initStoreInfo() async {
    final bool isAvailable = await _iap.isAvailable();
    _isAvailable = isAvailable;
    notifyListeners();

    if (!_isAvailable) {
      return;
    }

    final ProductDetailsResponse response = await _iap.queryProductDetails(_kIds);
    if (response.error == null) {
      _products = response.productDetails;
      notifyListeners();
    } else {
      if (kDebugMode) {
        print('IAP Query Error: ${response.error}');
      }
    }
  }

  Future<void> buyProduct(ProductDetails product) async {
    final PurchaseParam purchaseParam = PurchaseParam(productDetails: product);
    // For subscriptions, non-consumable
    await _iap.buyNonConsumable(purchaseParam: purchaseParam);
  }

  void _listenToPurchaseUpdated(List<PurchaseDetails> purchaseDetailsList) {
    for (final PurchaseDetails purchaseDetails in purchaseDetailsList) {
      if (purchaseDetails.status == PurchaseStatus.pending) {
        // Show pending UI
      } else {
        if (purchaseDetails.status == PurchaseStatus.error) {
          // Handle error
        } else if (purchaseDetails.status == PurchaseStatus.purchased ||
            purchaseDetails.status == PurchaseStatus.restored) {
          
          _verifyPurchase(purchaseDetails); // Verify and Deliver content
        }
        
        if (purchaseDetails.pendingCompletePurchase) {
          _iap.completePurchase(purchaseDetails);
        }
      }
    }
  }

  Future<void> _verifyPurchase(PurchaseDetails purchaseDetails) async {
    // IMPORTANT: In a real app, verify receipt with your backend!
    // For this simple implementation, we assume valid and unlock premium.
    _isPremium = true;
    notifyListeners();
  }

  void restorePurchases() {
    _iap.restorePurchases();
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
}
