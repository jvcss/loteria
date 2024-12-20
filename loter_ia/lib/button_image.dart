// Automatic FlutterFlow imports
import 'package:flutter/material.dart';
// Begin custom widget code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

class ImageIconButton extends StatefulWidget {
  const ImageIconButton({
    super.key,
    this.width = 50.0,
    this.height = 50.0,
    this.backgroundColor = Colors.white,
    this.borderRadius = 8.0,
    required this.imagePath,
  });

  final double width;
  final double height;
  final Color backgroundColor;
  final double borderRadius;
  final String imagePath;

  @override
  State<ImageIconButton> createState() => _ImageIconButtonState();
}

class _ImageIconButtonState extends State<ImageIconButton> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      height: widget.height,
      child: Material(
        color: widget.backgroundColor,
        borderRadius: BorderRadius.circular(widget.borderRadius),
        child: InkWell(
          borderRadius: BorderRadius.circular(widget.borderRadius),
          child: Center(
            child: Image.asset(
              widget.imagePath,
              fit: BoxFit.contain,
              width: widget.width * 0.6,
              height: widget.height * 0.6,
            ),
          ),
        ),
      ),
    );
  }
}

void main() {
  runApp(
    const MaterialApp(
      home: Scaffold(
        body: Center(
          child: ImageIconButton(
            width: 100,
            height: 100,
            imagePath: 'assets/images/flutterflow-icon.png',
          ),
        ),
      ),
    ),
  );
}