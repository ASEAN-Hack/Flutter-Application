class Catch{
  int cost;
  String fishType;
  String family;
  String genus;
  int weight;
  int quantity;

  Catch({
    this.cost,
    this.fishType,
    this.family,
    this.genus,
    this.weight,
    this.quantity
  }); 
}

class FishCard {
  double latitude;
  double longitude;
  int catchId;
  String date;
  int weight;
  List<Catch> catchesFish = [];

  FishCard({
    this.latitude,
    this.longitude,
    this.catchesFish
    });

}