"use client";

import { ReactNode } from "react";

interface TableHeaderProps {
  children: ReactNode;
}

export function TableHeader({ children }: TableHeaderProps) {
  return children;
} 