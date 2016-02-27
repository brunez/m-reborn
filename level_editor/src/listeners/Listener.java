package listeners;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import views.EditorPanel;
import views.ItemsPanel;
import controllers.EditorController;
import controllers.ItemsController;
import controllers.MainPanelController;

public class Listener implements MouseListener, MouseMotionListener, ActionListener, KeyListener, MouseWheelListener{

	private ItemsController itemsController;
	private EditorController editorController;
	private MainPanelController mainPanelController;

	public Listener(ItemsController itemsController,
			EditorController editorController,
			MainPanelController mainPanelController) {
		super();
		this.itemsController = itemsController;
		this.editorController = editorController;
		this.mainPanelController = mainPanelController;
	}

	@Override
	public void mouseDragged(MouseEvent ev) {
		if(ev.getSource().getClass() == EditorPanel.class){
			editorController.handleDrag(ev);
			editorController.update();
		}
	}

	@Override
	public void mouseMoved(MouseEvent ev) {
		if(ev.getSource().getClass() == EditorPanel.class){
			editorController.handleMove(ev);
		}		
		
	}

	@Override
	public void mouseClicked(MouseEvent ev) {
		
	}

	@Override
	public void mouseEntered(MouseEvent ev) {
		
		
	}

	@Override
	public void mouseExited(MouseEvent ev) {
		
		
	}

	@Override
	public void mousePressed(MouseEvent ev) {
		if(ev.getSource().getClass() == ItemsPanel.class){
			itemsController.handleClick(ev);
		} else if(ev.getSource().getClass() == EditorPanel.class){
			editorController.handleClick(ev);
		}
		
	}

	@Override
	public void mouseReleased(MouseEvent ev) {
		
		
	}

	@Override
	public void actionPerformed(ActionEvent ev) {
		if(ev.getActionCommand() == "increaseWidth"){
			editorController.increaseGridWidth();
			System.out.println("Got it");
		} else if(ev.getActionCommand() == "decreaseWidth"){
			editorController.decreaseGridWidth();
		} else if(ev.getActionCommand() == "increaseHeight"){
			editorController.increaseGridHeight();
		} else if(ev.getActionCommand() == "decreaseHeight"){
			editorController.decreaseGridHeight();
		} else if(ev.getActionCommand() == "toggleMode"){
			mainPanelController.toggleMode();
		} else if(ev.getActionCommand() == "exportLevel"){
			mainPanelController.dumpLevel();
		}
		
	}

	@Override
	public void keyPressed(KeyEvent ev) {
		editorController.handleKeyPress(ev);
	}

	@Override
	public void keyReleased(KeyEvent ev) {
		
		
	}

	@Override
	public void keyTyped(KeyEvent ev) {
		if(ev.getKeyCode() == KeyEvent.VK_SHIFT){
			editorController.toggleLineMode();
		}
		
	}

	@Override
	public void mouseWheelMoved(MouseWheelEvent ev) {		
		if(ev.getWheelRotation() > 0){
			itemsController.zoomOut();			
		} else {
			itemsController.zoomIn();			
		}
		editorController.update();
	}
	
}
