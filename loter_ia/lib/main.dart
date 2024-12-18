import 'package:flutter/material.dart';
import 'package:loter_ia/build_informations.dart';
import 'custom_line_chart.dart'; // Importe a classe CustomLineChart aqui

class ChartScreen extends StatelessWidget {
  const ChartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Exemplo de dados
    final List<double> totalPrizes = [5000000, 10000000, 7500000, 6000000, 8500000];
    final List<String> dates = ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05'];


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
