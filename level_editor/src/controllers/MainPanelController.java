package controllers;

import java.util.ArrayList;
import java.util.Iterator;

import models.Item;
import views.MainPanel;

public class MainPanelController {

	private MainPanel mainPanel;
	private EditorController editorController;
	private LevelDumper levelDumper;
	
	public MainPanelController() {
		super();
	}
	
	public void setMainPanel(MainPanel mp){
		this.mainPanel = mp;
	}
	
	public void setEditorController(EditorController ec){
		this.editorController = ec;
	}
	
	
	public void toggleMode(){
		mainPanel.toggleMode();
		editorController.toggleMode();
	}
	
	public void setMode(int mode){
		mainPanel.setMode(mode);
		editorController.setMode(mode);
	}
	
	public void dumpLevel(){
		ArrayList<Item> items = editorController.getItems();
		levelDumper = new LevelDumper();
		levelDumper.dump(items);
		
		
	}
	
}
