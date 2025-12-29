"use client";
import Image from "next/image";
import { Star } from "lucide-react"; // Make sure you have lucide-react installed
import type { Product, Rating } from "@types";
import { useQuery } from "@tanstack/react-query";
import { fetchProduct } from "@/lib/api";
import { useRouter, useSearchParams } from "next/navigation";
import { useCartStore } from "@/store/product.strore";


export default function Home() {
  const router = useRouter();
  const { data, isLoading, error } = useQuery({
    queryKey: ["products"],
    queryFn: fetchProduct,
  });

  const addToCart = useCartStore((state) => state.addToCart);
  const searchParams = useSearchParams();
   const selectedCategory = searchParams.get("category");
  const maxPriceParam = searchParams.get("maxPrice");
  const minRatingParam = searchParams.get("minRating");

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  const filterProducts = data.filter((product: Product) => {
    if (selectedCategory && product.category !== selectedCategory) {
      return false;
    }
    if (maxPriceParam) {
      if (product.price > maxPrice) {
        return false;
      }
    }
    if (minRatingParam) {
      if (product.rating.rate < minRating) {
        return false;
      }
    }
    return true;
  });

   const handleAddToCart = (product: Product) => {
    addToCart(product);       
    //router.push("/cart");    
  };
  return (
    <>
      <h1 className="text-3xl font-bold">Featured Products</h1>
      <div className="grid grid-cols-4 gap-6">
        {filterProducts.map((product: Product) => (
          <div
            key={product.id}
            className=" border rounded-lg p-4 bg-white hover:shadow-md transition-shadow flex flex-col"
          >
            <div className="relative w-full h-64 mb-4 overflow-hidden rounded-md bg-gray-50 flex items-center justify-center">
              <img
                src={product.image}
                alt={product.title}
                className="w-full h-full  p-4"
              />
            </div>

            <div className="flex flex-col flex-1">
              <span className="text-xl mb-1">{product.category}</span>
              <h2 className="font-semibold text-lg mb-2" title={product.title}>
                {product.title}
              </h2>

              <div className="flex items-center gap-1 mb-2">
                <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span className="text-sm ">{product.rating.rate}</span>
                <span className="text-sm ">({product.rating.count})</span>
              </div>

              <div className="mt-2 flex items-center justify-between pt-4">
                <span className="text-xl font-bold">${product.price}</span>
                <button  onClick={() => handleAddToCart(product)}className="bg-black text-white px-4 py-2 rounded-md cursor-pointer text-sm hover:bg-gray-800 ">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
