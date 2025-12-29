"use client";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./ui/collapsible";
import { Button } from "./ui/button";
import { useRouter, useSearchParams } from "next/navigation"; // 1. Import useSearchParams
import Link from "next/link";

// Menu items.
const menu = [
  {
    title: "Filters",
    url: "#",
  },
  {
    title: "Categories",
    url: "#",
    items: [
      { title: "Electronics",url:"/?category=electronics"},
      { title: "Jwelary",url:"/?category=jewelery"},
      { title: "Men's clothing",url:"/?category=men's clothing" },
      { title: "Women's clothing",url:"/?category=women's clothing"},
    ],
  },
  {
    title: "Price Range",
    url: "#",
    items: [
      { title: "$0",url:"/?maxPrice=50"},
      { title: "$154",url:"/?maxPrice=154" },
      { title: "$919",url:"/?maxPrice=919" },
      { title: "$1000",url:"/maxPrice=1000" },
    ],
  },
  {
    title: "Minimum Rating",
    url: "#",
     items: [
      { title: "4+ Star",url: "/?minRating=4" },
      { title: "3+ Star",url: "/?minRating=3" },
      { title: "2+ Star",url: "/?minRating=2" },
      { title: "1+ Star",url: "/?minRating=1"},
    ],
  },
];

export function AppSidebar() {
    const router = useRouter();
     const searchParams = useSearchParams(); // 2. Get current params

  // 3. Function to check if a specific menu item is active
  const checkActive = (url: string) => {
    // If url doesn't have query params, ignore
    if (!url.includes("?")) return false;
  }
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel></SidebarGroupLabel>
          <SidebarGroupContent>
             <SidebarMenu>
              {menu.map((item) => (
                <SidebarMenuItem key={item.title}>
                  {item.items && item.items.length > 0 ? (
                    <Collapsible className="group/collapsible" defaultOpen>
                      <CollapsibleTrigger asChild>
                        <SidebarMenuButton>
                          <span>{item.title}</span>
                        </SidebarMenuButton>
                      </CollapsibleTrigger>
                      <CollapsibleContent>
                        <SidebarMenuSub>
                          {item.items.map((subItem) => {
                            // 4. Determine if this item is active
                            const isActive = checkActive(subItem.url);

                            return (
                              <SidebarMenuSubItem key={subItem.title}>
                                <SidebarMenuSubButton 
                                  asChild 
                                  isActive={isActive} 
                                  className={isActive ? "bg-background-blue" : ""}
                                >
                                  {
                                  <Link href={subItem.url}>
                                    <span>{subItem.title}</span>
                                  </Link>
                                </SidebarMenuSubButton>
                              </SidebarMenuSubItem>
                            );
                          })}
                        </SidebarMenuSub>
                      </CollapsibleContent>
                    </Collapsible>
                  ) : (
                    <SidebarMenuButton asChild>
                      <Link href={item.url}>
                        <span className="font-medium">{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  )}
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
         <Button onClick={() => router.push("/")}>Clear Filters</Button>
      </SidebarContent>
    </Sidebar>
  );
}
