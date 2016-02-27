package controllers;

import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.util.ArrayList;

import models.Item;
import models.ItemType;
import views.EditorPanel;

public class EditorController {

	private EditorPanel editorPanel;

	public EditorController(){
		
	}
	
	public void setEditorPanel(EditorPanel editorPanel) {
		this.editorPanel = editorPanel;
	}
	
	public void setSelectedItem(ItemType item){
		this.editorPanel.setSelectedItem(item);
	}
	
	public void setMousePos(int x, int y){
		editorPanel.setMousePos(x, y);
	}	
	
	//TODO Ain't no better way?
	public void update(){
		editorPanel.repaint();
	}
	
	public void handleClick(MouseEvent ev){
		int button = ev.getButton();
		int x = ev.getX();
		int y = ev.getY();
		int mode = editorPanel.getMode();
		//A click was made
		if(button == MouseEvent.BUTTON1){
			//If we're in PLACE_ITEM mode
			if(mode == EditorPanel.PLACE_ITEM){
				//If we're in line mode (several items are to be added along a line)
				if(editorPanel.getLineMode()){
					this.placeMultipleItems();	
					//After we add the items, we deactivate line mode
					editorPanel.toggleLineMode();
				}
				//if we're not in line mode we just place the item in the square where the mouse is
				else{
					ItemType itemType = editorPanel.getSelectedItem();			
					this.placeItem(itemType, editorPanel.getGridMouseX(), editorPanel.getGridMouseY());
				}
			//If we're in SELECT mode
			} else {
				editorPanel.selectItem(editorPanel.getGridMouseX(), editorPanel.getGridMouseY());
				//TODO Line select mode
			}
		} else if(button == MouseEvent.BUTTON2){
			editorPanel.setOriginX(x);
			editorPanel.setOriginY(y);
		}
	}
	
	public void handleDrag(MouseEvent ev){
		int button = ev.getButton();
//		System.out.println(button);
//		System.out.println("Modifiers: " + ev.getModifiers());		
		if(ev.getModifiers() == MouseEvent.ALT_MASK){
			editorPanel.addMovementX(ev.getX() - editorPanel.getOriginX());
			editorPanel.addMovementY(ev.getY() - editorPanel.getOriginY());
			
			editorPanel.setOriginX(ev.getX());
			editorPanel.setOriginY(ev.getY());
		}
		
	}
	
	public void handleMove(MouseEvent ev){
		this.setMousePos(ev.getX(), ev.getY());
		this.update();
	}		
	
	public void handleKeyPress(KeyEvent ev){
		if(ev.getKeyCode() == KeyEvent.VK_SHIFT){
			this.toggleLineMode();
		} else if (ev.getKeyCode() == KeyEvent.VK_DELETE){
			this.deleteItems();
		} else if (ev.getKeyCode() == KeyEvent.VK_R){
			this.toggleRectangleMode();
		}
	}
	
	
	private void placeMultipleItems(){
		//Fetch the line origin and end
		int originX = editorPanel.getLine().getOriginX();
		int originY = editorPanel.getLine().getOriginY();
		int endX = editorPanel.getGridMouseX();
		int endY = editorPanel.getGridMouseY();
		//Fetch the item to be placed
		ItemType itemType = editorPanel.getSelectedItem();
		//Fetch how much has the panel been moved
		int movX = editorPanel.getMovementX();
		int movY = editorPanel.getMovementY();
		System.out.println("Line: " + originX + ", " + originY + ":" + endX + ", " + endY);
		
		//If the line is horizontal
		if (Math.abs(endX - originX) > 0){
			int direction;
			//Is the line headed right or left?
			if(endX > originX){
				direction = 1;
			} else {
				direction = -1;
			}
			int length = Math.abs(endX - originX);
			int position = originX;
			for(int i = 0; i <= length; i++){				
				this.placeItem(itemType, position, originY);				
				this.update();
				position += direction;
			}
		//If the line is vertical
		} else{
			int direction;
			//Is the line headed down or up?			
			if(endY > originY){
				direction = 1;
			} else {
				direction = -1;
			}
			int length = Math.abs(endY - originY);
			System.out.println("Line length: " + length);
			int position = originY;
			for(int i = 0; i <= length; i++){
				this.placeItem(itemType, originX, position);
				this.update();
				position += direction;				
			}
		}
	}
	
	public void toggleLineMode(){
		editorPanel.toggleLineMode();
	}
	
	public void toggleRectangleMode(){
		editorPanel.toggleRectangleMode();
	}
	
	public void placeItem(ItemType item, int x, int y){
		editorPanel.addItem(item, x, y);
		System.out.println("Placing item at " + x + ", " + y);
	}
	
	public void setMode(int mode){
		editorPanel.setMode(mode);
	}
	
	public void increaseGridWidth(){
		editorPanel.increaseGridWidth();
	}
	
	public void decreaseGridWidth(){
		editorPanel.decreaseGridWidth();
	}
	
	public void increaseGridHeight(){
		editorPanel.increaseGridHeight();
	}
	
	public void decreaseGridHeight(){
		editorPanel.decreaseGridHeight();
	}
	
	public void toggleMode(){
		editorPanel.toggleMode();
	}

	public void deleteItems(){
		editorPanel.deleteItems();
		this.update();
	}
	
	public ArrayList<Item> getItems(){
		return editorPanel.getItems();
	}
	
}
