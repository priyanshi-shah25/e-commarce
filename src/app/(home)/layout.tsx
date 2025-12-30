import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
//import { Navbar } from "@/components/navbar";

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SidebarProvider>
      <AppSidebar />
      {/* <Navbar/> */}
      <div className="flex w-full flex-col">
        <main className="p-4 flex-1">
          {children}
        </main>
      </div>
    </SidebarProvider>
  );
}