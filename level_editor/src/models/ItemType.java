package models;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

/**
 * This class represents an item type. It's used in the items panel 
 * to represent the different items you can place in the level.
 * @author Runo
 *
 */
public class ItemType {
	
	private String name;
	private BufferedImage image;
	private int posX;
	private int posY;
	//This variable indicates the congruence modulus 16.
	//It is used to designate a correct position to the image,
	//because the game grid tile size is 16.
	private int correction;
	
	public ItemType(String name, String imagePath) {
		super();
		this.name = name;
		try {
			this.image = ImageIO.read(new File(imagePath));
		} catch (IOException e) {
			System.out.println("Failed to read " + imagePath);
			e.printStackTrace();
		}
		
		correction = image.getHeight() % 16;
	}
	
	public BufferedImage getImage(){
		return this.image;				
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
	
	public int getWidth(){
		return image.getWidth();
	}
	
	public int getHeight(){
		return image.getHeight();
	}

	public int getCorrection(){
		return correction;
	}
	
	public String getName(){
		return name;
	}
	
}
