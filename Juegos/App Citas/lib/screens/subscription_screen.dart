
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:in_app_purchase/in_app_purchase.dart';
import '../services/purchase_service.dart';

class SubscriptionScreen extends StatefulWidget {
  const SubscriptionScreen({super.key});

  @override
  State<SubscriptionScreen> createState() => _SubscriptionScreenState();
}

class _SubscriptionScreenState extends State<SubscriptionScreen> {
  @override
  void initState() {
    super.initState();
    // Initialize store info when screen loads
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PurchaseService>().initialize();
    });
  }

  @override
  Widget build(BuildContext context) {
    final purchaseService = context.watch<PurchaseService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Premium Subscription'),
      ),
      body: purchaseService.isPremium
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.check_circle, color: Colors.green, size: 64),
                  SizedBox(height: 16),
                  Text('You are a Premium Member!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                ],
              ),
            )
          : SingleChildScrollView(
              child: Column(
                children: [
                  const SizedBox(height: 20),
                  const Icon(Icons.star, color: Colors.amber, size: 80),
                  const SizedBox(height: 16),
                  const Text(
                    'Upgrade to Premium',
                    style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                  ),
                  const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Text(
                      'Unlock unlimited swipes, see who likes you, and more!',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                  const Divider(),
                  if (!purchaseService.isAvailable)
                    const Padding(
                      padding: EdgeInsets.all(16.0),
                      child: Text('Store not available'),
                    )
                  else if (purchaseService.products.isEmpty)
                    const Padding(
                      padding: EdgeInsets.all(16.0),
                      child: CircularProgressIndicator(),
                    )
                  else
                    ...purchaseService.products.map(
                      (product) => ListTile(
                        title: Text(product.title),
                        subtitle: Text(product.description),
                        trailing: FilledButton(
                          onPressed: () {
                            purchaseService.buyProduct(product);
                          },
                          child: Text(product.price),
                        ),
                      ),
                    ),
                  const SizedBox(height: 20),
                  TextButton(
                    onPressed: () {
                      purchaseService.restorePurchases();
                    },
                    child: const Text('Restore Purchases'),
                  ),
                ],
              ),
            ),
    );
  }
}
