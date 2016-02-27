package controllers;

import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.Iterator;

import models.ItemType;
import views.EditorPanel;
import views.ItemsPanel;

public class ItemsController {

	private ItemsPanel itemsPanel;
	private EditorController editorController;
	private MainPanelController mainPanelController;

	public ItemsController(){
		
	}
	
	public void setItemsPanel(ItemsPanel itemsPanel) {
		this.itemsPanel = itemsPanel;
	}
	
	public void setEditorController(EditorController editorController) {
		this.editorController = editorController;
	}
	
	public void setMainPanelController(MainPanelController mainPanelController) {
		this.mainPanelController = mainPanelController;
	}	
	
	/**
	 * Handle clicks on items
	 * @param x
	 * @param y
	 */
	public void handleClick(MouseEvent ev){
		int x = ev.getX();
		int y = ev.getY();
		int button = ev.getButton();
		System.out.println("Click at " + x + ", " + y);
		
		if(button  == MouseEvent.BUTTON1){
			ArrayList<ItemType> list = itemsPanel.getItemTypes();
			Iterator<ItemType> it = list.iterator();
			ItemType target;
			boolean foundTarget = false;
			/**
			 * Figure out where was the click made. If it was on an item, set it as selected item.
			 */
			while(it.hasNext() && !foundTarget){
				ItemType itemType = it.next();
				int posX = itemType.getPosX();
				int posY = itemType.getPosY();
				int width = itemType.getWidth()*ItemsPanel.ZOOM;
				int height = itemType.getHeight()*ItemsPanel.ZOOM;
				if(x >= posX && x < posX+width && y >= posY && y < posY+height){
					target = itemType;
					foundTarget = true;
					editorController.setSelectedItem(target);
//					editorController.setMode(EditorPanel.PLACE_ITEM);
					mainPanelController.setMode(EditorPanel.PLACE_ITEM);
					System.out.println("Set target");
				}
			}
		}
	}

	public void zoomIn(){
		itemsPanel.zoomIn();
	}
	
	public void zoomOut(){
		itemsPanel.zoomOut();
	}
	
}
