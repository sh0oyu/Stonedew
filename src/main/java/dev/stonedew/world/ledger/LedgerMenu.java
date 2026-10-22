package dev.stonedew.world.ledger;

import dev.stonedew.core.ModContent;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;

public final class LedgerMenu extends AbstractContainerMenu {
  private final ContainerLevelAccess access;

  public LedgerMenu(int id, Inventory inventory) {
    this(id, inventory, ContainerLevelAccess.NULL);
  }

  public LedgerMenu(int id, Inventory inventory, ContainerLevelAccess access) {
    super(ModContent.LEDGER_MENU.get(), id);
    this.access = access;
  }

  @Override
  public ItemStack quickMoveStack(Player player, int slot) {
    return ItemStack.EMPTY;
  }

  @Override
  public boolean stillValid(Player player) {
    return stillValid(access, player, ModContent.LEDGER.get());
  }
}
