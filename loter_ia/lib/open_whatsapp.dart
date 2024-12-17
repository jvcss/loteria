import 'package:url_launcher/url_launcher.dart';

Future<void> openWhatsApp(String phoneNumber, String message) async {
  // Construct the WhatsApp URL
  final Uri whatsappUri = Uri.parse('https://wa.me/$phoneNumber?text=${Uri.encodeComponent(message)}');

  // Check if the URL can be launched
  if (await canLaunchUrl(whatsappUri)) {
    await launchUrl(whatsappUri, mode: LaunchMode.externalApplication);
  } else {
    throw 'Could not launch $whatsappUri';
  }
}