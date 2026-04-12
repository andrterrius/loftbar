import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import TelegramSdkInit from "@/components/TelegramSdkInit";
import InitTelegramAuth from "@/components/auth/initTelegramAuth";
import AuthGate from "@/components/auth/AuthGate";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


export default function RootLayout({ children }) {
  
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <TelegramSdkInit />
        <InitTelegramAuth/>
        <AuthGate>{children}</AuthGate>
      </body>
    </html>
  );
}
