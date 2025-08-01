import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/components/context-provider/auth-provider";

export const metadata: Metadata = {
  title: "Git seed",
  description: "Work on projects securely",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
