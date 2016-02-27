package views;

import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Iterator;

import javax.swing.JPanel;

import listeners.Listener;
import models.ItemType;

public class ItemsPanel extends JPanel{
	
	private ArrayList<ItemType> itemTypes;
	private int currentX;
	private int currentY;
	private int currentMaxY;
	
	public static int ZOOM = 2;
	
	public ItemsPanel(Listener listener){
		
		this.addMouseListener(listener);
		
		itemTypes = new ArrayList<ItemType>();
		try {
			this.readFile(itemTypes);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		this.setBackground(Color.WHITE);
		
		currentX = 0;
		currentY = 0;
		currentMaxY = 0;
		
		repaint();
//		this.setPreferredSize(new Dimension(1000, 1000));
		
	}
	
	@Override
	protected void paintComponent(Graphics g){
		super.paintComponent(g);
		g.clearRect(0, 0, this.getWidth(), this.getHeight());
		Iterator<ItemType> it = itemTypes.iterator();
		while(it.hasNext()){
			ItemType itemType = it.next();

			BufferedImage resizedImage = ItemsPanel.resizeImage(itemType.getImage(), itemType.getWidth()*ZOOM, itemType.getHeight()*ZOOM);
//			System.out.println("Drawing at " + itemType.getPosX() + ", " + itemType.getPosY());
			g.drawImage(resizedImage, itemType.getPosX(), itemType.getPosY(), null);

		}
		
		
	}

	public static BufferedImage resizeImage(final Image image, int width, int height) {
        final BufferedImage bufferedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        final Graphics2D graphics2D = bufferedImage.createGraphics();
        graphics2D.setComposite(AlphaComposite.Src);
        graphics2D.drawImage(image, 0, 0, width, height, null);
        graphics2D.dispose();
 
        return bufferedImage;
    }
	
	private void readFile(ArrayList<ItemType> list) throws IOException{
		FileInputStream fis = new FileInputStream(new File("images" + File.separator+ "items.txt"));
		InputStreamReader isr = new InputStreamReader(fis);
		BufferedReader br = new BufferedReader(isr);
		
		String line;
		while((line = br.readLine()) != null){
			if(line.matches(".+:.+")){
				String[] parts = line.split(":");
				String name = parts[0];
				String image = parts[1].replace("\\", File.separator);
				list.add(new ItemType(name, image));
			}
		}
	}
	
	public void organizeItems(){
		Iterator<ItemType> it = itemTypes.iterator();
		while(it.hasNext()){
			
			ItemType itemType = it.next();
			//Calculate the position of the image. If it exceeds the area,
			//next row
			BufferedImage resizedImage = ItemsPanel.resizeImage(itemType.getImage(), itemType.getWidth()*ZOOM, itemType.getHeight()*ZOOM);
//			System.out.println("Got an image of " + resizedImage.getWidth() + ", " + resizedImage.getHeight());
//			System.out.println("Panel width = " + this.getWidth());
			if(currentX + resizedImage.getWidth() > this.getWidth()){
				currentX = 0;
				currentY = currentMaxY;
			}
			//Calculate the maximum Y value, so that the next row 
			//does not overlap the current one
			if(currentY + resizedImage.getHeight() > currentMaxY){
				currentMaxY = currentY + resizedImage.getHeight();
			}
			
			itemType.setPosX(currentX);
			itemType.setPosY(currentY);
			
//			System.out.println("Set pos at " + currentX + ", " + currentY);
			currentX = currentX + resizedImage.getWidth();

		}
		
		currentX = 0;
		currentY = 0;
		

	}
	
	public void zoomIn(){		
		ZOOM++;
		
	}
	
	public void zoomOut(){
		if(ZOOM > 1){
			ZOOM--;
		}
	}
	
	public ArrayList<ItemType> getItemTypes(){
		return itemTypes;
	}
	
}
