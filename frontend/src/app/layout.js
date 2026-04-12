import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";
import "./globals.css";
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
      <head>
        <Script
          src="/telegram-web-app.js"
          strategy="beforeInteractive"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <InitTelegramAuth/>
        <AuthGate>{children}</AuthGate>
      </body>
    </html>
  );
}
