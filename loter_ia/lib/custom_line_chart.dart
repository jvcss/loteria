import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class CustomLineChart extends StatelessWidget {
  final List<double> totalPrizes; // Dados para o eixo Y
  final List<String> dates; // Dados para o eixo X

  const CustomLineChart({
    required this.totalPrizes,
    required this.dates,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: LineChart(
        LineChartData(
          gridData: FlGridData(
            show: true,
            drawHorizontalLine: true,
            drawVerticalLine: false,
            horizontalInterval: 5000000, // Intervalo das linhas horizontais
            getDrawingHorizontalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.5),
              strokeWidth: 1,
              dashArray: [5, 5],
            ),
          ),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (value, meta) => Text(
                  '\$${(value / 1000000).toStringAsFixed(1)}M',
                  style: const TextStyle(fontSize: 12, color: Colors.blueGrey),
                ),
                reservedSize: 40,
              ),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (value, meta) {
                  int index = value.toInt();
                  if (index < 0 || index >= dates.length) {
                    return const SizedBox();
                  }
                  return Transform.rotate(
                    angle: -0.5, // Inclina o texto no eixo X
                    child: Text(
                      dates[index],
                      style:
                          const TextStyle(fontSize: 10, color: Colors.blueGrey),
                    ),
                  );
                },
                reservedSize: 32,
                interval: 1, // Intervalo das labels no eixo X
              ),
            ),
            // ignore: prefer_const_constructors
            topTitles: AxisTitles(),
          ),
          borderData: FlBorderData(
            show: true,
            border: Border.all(
              color: Colors.grey,
              width: 1,
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: totalPrizes
                  .asMap()
                  .entries
                  .map((entry) => FlSpot(entry.key.toDouble(), entry.value))
                  .toList(),
              isCurved: true,
              color: Colors.blueAccent,
              barWidth: 4,
              isStrokeCapRound: true,
              belowBarData: BarAreaData(
                show: true,
                gradient: LinearGradient(
                  colors: [
                    Colors.blueAccent.withOpacity(0.4),
                    Colors.blueAccent.withOpacity(0.1),
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ),
              dotData: FlDotData(
                show: true,
                getDotPainter: (spot, percent, barData, index) =>
                    FlDotCirclePainter(
                  radius: 4,
                  color: Colors.blue,
                  strokeWidth: 2,
                  strokeColor: Colors.white,
                ),
              ),
            ),
          ],
          lineTouchData: LineTouchData(
            touchTooltipData: LineTouchTooltipData(
              getTooltipColor: (spot) => Colors.blueGrey.withOpacity(0.7),
              getTooltipItems: (touchedSpots) {
                return touchedSpots.map((spot) {
                  return LineTooltipItem(
                    '${dates[spot.spotIndex]}: \$${spot.y.toStringAsFixed(2)}',
                    const TextStyle(color: Colors.white),
                  );
                }).toList();
              },
            ),
            touchCallback: (event, response) {
              if (response == null || response.lineBarSpots == null) return;
              for (var spot in response.lineBarSpots!) {
                print(
                    'Selected: Date: ${dates[spot.spotIndex]}, Value: ${spot.y}');
              }
            },
          ),
        ),
      ),
    );
  }
}
