//TODO Big todo: Concentrar all mode changes in one class.
package controllers;

import javax.swing.SwingUtilities;

import listeners.Listener;
import views.MainWindow;

public class Main {

	private Listener listener;
	private ItemsController itemsController;
	private EditorController editorController;
	private MainPanelController mainPanelController;
	
	public Main(){		
		itemsController = new ItemsController();
		editorController = new EditorController();
		mainPanelController = new MainPanelController();
		itemsController.setEditorController(editorController);
		itemsController.setMainPanelController(mainPanelController);
		listener = new Listener(itemsController, editorController, mainPanelController);
		new MainWindow(listener, itemsController, editorController, mainPanelController);
	}
	
	public static void main(String[] args){
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){				
				new Main();
			}
		});
	}
	
}
