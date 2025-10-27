with entry {
  jay_prices: list[int] = [];
  
  #dictionaries- key  & value pair
  jay_quantities: dict[str, int] = {
    "Shirt": 5,
    "Short": 2,
    "Jacket": 4
  };

  #set implementation
  shopping_cart_unique: set[str] = {"shirt", "shirt", "short", "short", "jacket"};
  
  #list comprehension
  prices: list[int] = [500, 800, 1000, 1200, 300, 450, 750, 950, 350];

  discounted_prices: list[int] = [price for price in prices if price >= 700];

  #append to list
  jay_prices.append(250);
  jay_prices.append(350);
  jay_prices.append(500);

  first_price: int = jay_prices[0];
  print(f"This is the first price: {first_price}");
  
  print(f"jay prices: {jay_prices}");

  print(f"The number of shirts bought: {jay_quantities["Shirt"]}");
  print(f"The number of shorts bought: {jay_quantities["Short"]}");
  print(f"The number of jarckets bought: {jay_quantities["Jacket"]}");
  print(f"The shopping cart contains: {shopping_cart_unique}");
  print(f"Items with prices in this list are discouted: {discounted_prices}");
}