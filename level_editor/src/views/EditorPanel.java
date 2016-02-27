package views;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import javax.swing.JPanel;

import listeners.Listener;
import models.Item;
import models.ItemType;

public class EditorPanel extends JPanel{
	
	private int mode;
	private int gridWidth;
	private int gridHeight;
	
	//TODO Replace with TILE_SIZE and multiplier
	private int tileSize;
	private final int BASE_TILE_SIZE = 16;
	
	private boolean lineMode;
	private Line line;
	private boolean rectangleMode;
	private Rectangle rectangle;
//	private int lineOriginX;
//	private int lineOriginY;
	
	/**
	 * Mode constants
	 */
	public static final int SELECT = 0;
	public static final int PLACE_ITEM = 1;
	
	/**
	 * Elements added to the level
	 */
	private ArrayList<Item> items;
	private HashMap<String, Item> itemsMap;
	
	private int movementX;
	private int movementY;
	private int originX;
	private int originY;
	
	private ItemType selectedItem;
	private int mouseX;
	private int mouseY;
	
	
	public EditorPanel(Listener listener, int mode){

		this.addMouseListener(listener);
		this.addMouseMotionListener(listener);
		//TODO Zooming
//		this.addMouseWheelListener(listener);
		this.addKeyListener(listener);
		
		this.setBackground(Color.WHITE);
		
		movementX = 0;
		movementY = 0;
		
		items = new ArrayList<Item>();
		itemsMap = new HashMap<String, Item>();
		mouseX = 0;
		mouseY = 0;
		
		this.mode = mode;
		System.out.println("Created with mode " + mode);
		tileSize = 32;
		gridWidth = 264;
		gridHeight= 14;
		lineMode = false;
		line = new Line();
		rectangle = new Rectangle();
		
		
	}
	
	protected void paintComponent(Graphics g){
		super.paintComponent(g);
		
		/**
		 * Draw the grid
		 */
		g.setColor(Color.GRAY);
		for(int i = 0; i <= gridHeight; i++){
			g.drawLine(0+movementX, i*tileSize+movementY, gridWidth*tileSize+movementX, i*tileSize+movementY);
		}
		for(int i = 0; i <= gridWidth; i++){
			g.drawLine(i*tileSize+movementX, 0+movementY, i*tileSize+movementX, gridHeight*tileSize+movementY);
		}
		
		
		/**
		 * Draw the items. The position is multiplied by the tile size (default = 32) for them to appear correctly.
		 */		
		Iterator<Item> it = items.iterator();		
		while(it.hasNext()){
			Item item = it.next();
			if(item != null){
				BufferedImage resizedImage = ItemsPanel.resizeImage(item.getImage(), item.getWidth()*ItemsPanel.ZOOM, item.getHeight()*ItemsPanel.ZOOM);
				//TODO Replace correction*2 with multiplier
				g.drawImage(resizedImage, item.getPosX()*tileSize + movementX, item.getPosY()*tileSize + movementY - item.getItemType().getCorrection()*2, null);
				
				if(item.isSelected()){
					g.setColor(Color.RED);
					g.drawRect(item.getPosX()*tileSize + movementX, item.getPosY()*tileSize + movementY, tileSize, tileSize);
					g.drawRect(item.getPosX()*tileSize + movementX-1, item.getPosY()*tileSize + movementY-1, tileSize, tileSize);
					g.drawRect(item.getPosX()*tileSize + movementX+1, item.getPosY()*tileSize + movementY+1, tileSize, tileSize);
				}
			}
//			System.out.println("Item at " + item.getPosX() + ", " + item.getPosY());
		}
		
		if(mode == SELECT){
			//TODO Make this work!
			if(rectangleMode){
				//TODO Ends are wrong
				rectangle.setEndX(this.getGridMouseX()*32+movementX%32);
				rectangle.setEndY(this.getGridMouseY()*32+movementX%32);
				g.setColor(Color.BLUE);
				g.drawRect(rectangle.getOriginX()*tileSize+movementX, rectangle.getOriginY()*tileSize+movementY,rectangle.getEndX(),rectangle.getEndY());
			}
		}
		
		/**
		 * Draw the item that was selected in the items panel
		 */
		if(mode == PLACE_ITEM){
//			System.out.println("Mode: " + this.mode);
			//TODO Try to fix this. It's dirty.
			if(selectedItem != null){
				//TODO stuck the resized image into the itemType object
				//TODO correct mouse pos when movement is not 0
				BufferedImage resizedImage = ItemsPanel.resizeImage(selectedItem.getImage(), selectedItem.getWidth()*ItemsPanel.ZOOM, selectedItem.getHeight()*ItemsPanel.ZOOM);
				g.drawImage(resizedImage, this.getGridMouseX()*tileSize+movementX, this.getGridMouseY()*tileSize+movementY-selectedItem.getCorrection()*2, null);
			}
		}	
		
		/**
		 * Draw the line in line mode
		 */
		if(lineMode){
			g.setColor(Color.black);
			int horizontalLength = Math.abs(mouseX - (line.getOriginX()*tileSize+movementX));
			int verticalLength = Math.abs(mouseY - (line.getOriginY()*tileSize+movementY));
						
			if(horizontalLength > verticalLength){ //Horizontal line
				g.drawLine(line.getOriginX()*tileSize+movementX+(tileSize/2), line.getOriginY()*tileSize+(tileSize/2)+movementY, this.toGameCoords(mouseX)*tileSize, line.getOriginY()*tileSize+(tileSize/2)+movementY);				
			} else if(horizontalLength < verticalLength){ //Vertical line
				g.drawLine(line.getOriginX()*tileSize+movementX+(tileSize/2), line.getOriginY()*tileSize+movementY+(tileSize/2), line.getOriginX()*tileSize+movementX+(tileSize/2), this.toGameCoords(mouseY)*tileSize);
			} else{ //TODO Diagonal line
				g.drawLine(line.getOriginX()*tileSize+movementX, line.getOriginY()*tileSize+(tileSize/2)+movementY, this.toGameCoords(mouseX)*tileSize, this.toGameCoords(mouseX)*tileSize);
			}
			
			//Draw the line length
			line.setEndX(this.getGridMouseX());
			line.setEndY(this.getGridMouseY());
			g.setFont(new Font("Arial", Font.BOLD, 48));
			g.drawString(Integer.toString(line.getLength()+1), mouseX+50, mouseY+25);
		}
		
		
		//TODO Proper focus request
		this.requestFocusInWindow();
	}

	public void toggleLineMode(){
		lineMode = !lineMode;
		if(lineMode){
			line.setOriginX((mouseX-movementX)/tileSize);
			line.setOriginY((mouseY-movementY)/tileSize);
//			System.out.println("Line Origin: " + line.getOriginX() + ", " + line.getOriginY());
		}
	}
	
	public void toggleRectangleMode(){
		if(this.mode == SELECT){
			rectangleMode = !rectangleMode;
			rectangle.setOriginX((mouseX-movementX)/tileSize);
			rectangle.setOriginY((mouseY-movementY)/tileSize);
		}
	}
	
	public int toGameCoords(int coord){
		return coord/tileSize;
	}
	
	public int toRealCoords(int coord){
		return coord*tileSize;
	}
	
	public boolean getLineMode(){
		return lineMode;
	}
		
	public ItemType getSelectedItem(){
		return selectedItem;
	}
	
	public void setSelectedItem(ItemType item){
		this.selectedItem = item;
		System.out.println("EditorPanel: set selected item");
	}
	
	public void addItem(ItemType itemType, int x, int y){
		//TODO Check if it's occupied - Overwrite or do nothing?
		Item item = new Item(itemType, x, y);
		 items.add(item);		 
		 itemsMap.put(x+","+y, item);
	}
	
	public void setMousePos(int x, int y){
		mouseX = x;
		mouseY = y;
//		System.out.println("MousePos: " + x + ", " + y);
	}
	
	public int getMode(){
		return mode;
	}
	
	public void setMode(int mode){
		this.mode = mode;
	}

	public void setOriginX(int originX) {
		this.originX = originX;
	}

	public void setOriginY(int originY) {
		this.originY = originY;
	}
	
	public int getOriginX() {
		return originX;
	}

	public int getOriginY() {
		return originY;
	}
	
	public void setMovementX(int x){
		movementX = x;
	}
	
	public void setMovementY(int y){
		movementY = y;
	}
	
	public void addMovementX(int x){
		movementX += x;
//		System.out.println("Movx = " + movementX);
	}
	
	public void addMovementY(int y){
		movementY += y;
	}
	
	public int getMovementX() {
		return movementX;
	}

	public int getMovementY() {
		return movementY;
	}
	
	public int getGridMouseX(){
		return this.toGameCoords(mouseX-movementX);
	}
	
	public int getGridMouseY(){
		return this.toGameCoords(mouseY-movementY);
	}

	public int getTileSize(){
		return tileSize;
	}
	
	public int getGridWidth(){
		return gridWidth;
	}
	
	public int getGridHeight(){
		return gridHeight;
	}	
	
	public void increaseGridWidth(){
		gridWidth++;
		repaint();
	}
	
	public void decreaseGridWidth(){
		if(gridWidth > 0){
			gridWidth--;
		}
		repaint();
	}
	
	public void increaseGridHeight(){
		gridHeight++;
		repaint();
	}
	
	public void decreaseGridHeight(){
		if(gridHeight > 0){
			gridHeight--;
		}
		repaint();
	}
	
	public Line getLine(){
		return line;
	}
	
	public void toggleMode(){
		if(this.mode == SELECT){
			this.mode = PLACE_ITEM;
		} else if (this.mode == PLACE_ITEM){
			this.mode = SELECT;
		}
	}

	public void selectItem(int x, int y){
		Item item = itemsMap.get(x+","+y);
		if(item != null){
			item.setSelected(!item.isSelected());
		}
	}

	public void deleteItems(){
		ArrayList<Item> garbageCan = new ArrayList<Item>();
		//First, we check which items are selected and we store them in a new list
		Iterator<Item> it = items.iterator();		
		while(it.hasNext()){
			Item item = it.next();
			if(item.isSelected()){
				garbageCan.add(item);
			}
		}
		//Then, we go through that list and we remove all its elements from the original one
		it = garbageCan.iterator();
		while(it.hasNext()){
			items.remove(it.next());
		}
	}
	
	public ArrayList<Item> getItems(){
		return items;
	}
}
