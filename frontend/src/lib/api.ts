export const fetchProduct = async () => {
  const res = await fetch("https://fakestoreapi.com/products");

  if (!res.ok) {
    console.log("Failed to fetch products");
  }
  return res.json()
}