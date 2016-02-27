package views;

import javax.swing.JFrame;

import listeners.Listener;
import controllers.EditorController;
import controllers.ItemsController;
import controllers.MainPanelController;

public class MainWindow extends JFrame{

	private MainPanel mainPanel;

	
	public MainWindow(Listener listener, ItemsController ic, EditorController ec, MainPanelController mpc){
		
		mainPanel = new MainPanel(listener, ic, ec);		
		mpc.setMainPanel(mainPanel);
		mpc.setEditorController(ec);
		
	   	this.add(mainPanel);
	   	
		this.setSize(1280, 900);
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		this.setVisible(true);
		
		mainPanel.getReady();
	}
}
