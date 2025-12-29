import { create } from "zustand";
import { CartState } from "@/types/product";

export const useCartStore = create<CartState>((set) => ({
  cart: [],
  addToCart: (product) => set((state) => ({ 
    cart: [...state.cart, product] 
  })),
}));