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
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./ui/collapsible";
import { Button } from "./ui/button";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
const menu = [
  {
    title: "Filters",
    url: "#",
  },
  {
    title: "Categories",
    url: "#",
    items: [
      { title: "Electronics", url: "/?category=electronics" },
      { title: "Jwelary", url: "/?category=jewelery" },
      { title: "Men's clothing", url: "/?category=men's clothing" },
      { title: "Women's clothing", url: "/?category=women's clothing" },
    ],
  },
  {
    title: "Price Range",
    url: "#",
    items: [
      { title: "$50", url: "/?maxPrice=50" },
      { title: "$154", url: "/?maxPrice=154" },
      { title: "$919", url: "/?maxPrice=919" },
      { title: "$1000", url: "/?maxPrice=1000" },
    ],
  },
  {
    title: "Minimum Rating",
    url: "#",
    items: [
      { title: "⭐⭐⭐⭐4+ Star", url: "/?minRating=4" },
      { title: "⭐⭐⭐3+ Star", url: "/?minRating=3" },
      { title: "⭐⭐2+ Star", url: "/?minRating=2" },
      { title: "⭐1+ Star", url: "/?minRating=1" },
    ],
  },
];

export function AppSidebar() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const checkActive = (url: string) => {
  const query = url.split("?")[1];

  const [key, value] = query.split("=");
  return searchParams.get(key) === value;
  };

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
                            const isActive = checkActive(subItem.url);

                            return (
                              <SidebarMenuSubItem key={subItem.title}>
                                <SidebarMenuSubButton
                                  asChild
                                  isActive={isActive}
                                  className={
                                    isActive
                                      ? " font-bold"
                                      : ""
                                  }
                                >
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
        <Button
          className="m-4 p-3 cursor-pointer"
          onClick={() => router.push("/")}
        >
          Clear Filters
        </Button>
      </SidebarContent>
    </Sidebar>
  );
}
