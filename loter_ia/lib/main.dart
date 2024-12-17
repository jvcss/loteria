import 'package:flutter/material.dart';
import 'package:loter_ia/build_informations.dart';
import 'custom_line_chart.dart'; // Importe a classe CustomLineChart aqui

class ChartScreen extends StatelessWidget {
  const ChartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Testando calculateHitsWithPrizes
    final officialResults, generatedResults, hitsWithPrizes = chartActivity();

    // Testando calculateFrequency
    List<Map<String, dynamic>> frequency = calculateFrequency(hitsWithPrizes);
    print('\nFrequency:');
    frequency.forEach((freq) => print(freq));
    // Testando calculateEachTotalPrize
    List<Map<String, dynamic>> totalPrizes = calculateEachTotalPrize(frequency);
    print('\nTotal Prizes:');
    totalPrizes.forEach((prize) => print(prize));
    print('\n\n\n\n\n\n\n\n:');

    return Scaffold(
      appBar: AppBar(title: const Text('Gráfico Customizado')),
      body: Center(
        child: CustomLineChart(
          totalPrizes: totalPrizes,
          dates: dates,
        ),
      ),
    );
  }
}

void main() {
  runApp(
    const MaterialApp(
      home: ChartScreen(),
    ),
  );
}
