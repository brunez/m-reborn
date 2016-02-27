package models;

import java.awt.image.BufferedImage;

public class Item {

	private int posX;
	private int posY;
	private ItemType itemType;
	private boolean selected;

	public Item(ItemType itemType, int posX, int posY) {
		super();
		this.posX = posX;
		this.posY = posY;
		this.itemType = itemType;
		
		this.selected= false;
	}
	
	public BufferedImage getImage(){
		return itemType.getImage();
	}
	
	public ItemType getItemType(){
		return itemType;
	}
	
	public int getWidth(){
		return itemType.getImage().getWidth();
	}
	
	public int getHeight(){
		return itemType.getImage().getHeight();
	}

	public int getPosX() {
		return posX;
	}

	public void setPosX(int posX) {
		this.posX = posX;
	}

	public int getPosY() {
		return posY;
	}

	public void setPosY(int posY) {
		this.posY = posY;
	}
	
	public boolean isSelected() {
		return selected;
	}

	public void setSelected(boolean selected) {
		this.selected = selected;
	}	
	
}
