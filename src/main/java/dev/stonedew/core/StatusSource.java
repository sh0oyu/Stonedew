package dev.stonedew.core;

/** Machines and plants expose language keys; client UI translates them. */
public interface StatusSource {
  String getStatusReason();
}
