"use client";

import { Button } from "@/components/ui/button";
import { useCartStore } from "@/store/product.strore";
import Link from "next/link";

export default function CartPage() {
  
  const cart = useCartStore((state) => state.cart);

  if (cart.length === 0) {
    return (
      <div className="p-10 text-center">
        <h2 className="text-2xl font-bold">Your Cart is Empty</h2>
        <Link href="/" className="text-blue-500 underline mt-4 block">
          Go back to shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
      <div className="space-y-4">
        {cart.map((product, index) => (

          <div key={`${product.id}-${index}`} className="flex items-center gap-4 border p-4 rounded-lg">
            <div className="w-20 h-20 relative">
               <img src={product.image} alt={product.title} className="w-full h-full" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold">{product.title}</h3>
              <p className="text-gray-500">${product.price}</p>
            </div>
            <Button>Proceed to Buy </Button>
          </div>
        ))}
      </div>
    </div>
  );
}