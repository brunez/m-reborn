package views;

import java.awt.Dimension;

import javax.swing.BorderFactory;
import javax.swing.GroupLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.border.BevelBorder;
import javax.swing.border.Border;

import listeners.Listener;
import controllers.EditorController;
import controllers.ItemsController;

public class MainPanel extends JPanel{

	private EditorPanel innerEditorPanel;
	private ItemsPanel innerItemsPanel;
	
	//TODO Menu en otra clase
	private JPanel topPanel;
	private JMenu menu;
	private JButton increaseWidth;
	private JButton decreaseWidth;
	private JButton increaseHeight;
	private JButton decreaseHeight;
	private JButton toggleMode;
	private JLabel modeLabel;
	private JButton exportLevel;
	
	private JScrollPane editorPanel;
	private JScrollPane itemsPanel;
	private GroupLayout layout;
	
	/**
	 * Mode names
	 */
	private final String[] modeNames = {"Select", "Place item"}; 
	private int modeIndex;

	
	public MainPanel(Listener listener, ItemsController ic, EditorController ec){
		//TODO quitar listener del constructor
		innerEditorPanel = new EditorPanel(listener, EditorPanel.SELECT);			
		innerItemsPanel = new ItemsPanel(listener);
		editorPanel = new JScrollPane(innerEditorPanel);
		editorPanel.setPreferredSize(new Dimension(800, 200));
		
		/**
		 * Components
		 */
		topPanel = new JPanel();
		menu = new JMenu("File");			
		topPanel.add(menu);
		increaseWidth = new JButton("Increase Width");
		increaseWidth.setActionCommand("increaseWidth");
		increaseWidth.addActionListener(listener);
		decreaseWidth = new JButton("Decrease Width");
		decreaseWidth.setActionCommand("decreaseWidth");
		decreaseWidth.addActionListener(listener);
		topPanel.add(increaseWidth);
		topPanel.add(decreaseWidth);
		increaseHeight = new JButton("Increase Height");
		increaseHeight.setActionCommand("increaseHeight");
		increaseHeight.addActionListener(listener);
		decreaseHeight= new JButton("Decrease Height");
		decreaseHeight.setActionCommand("decreaseHeight");
		decreaseHeight.addActionListener(listener);
		toggleMode = new JButton("Toggle Mode");
		toggleMode.setActionCommand("toggleMode");
		toggleMode.addActionListener(listener);
		exportLevel = new JButton("Export Level");
		exportLevel.setActionCommand("exportLevel");
		exportLevel.addActionListener(listener);
	   	
	   	modeIndex = 0;		
		modeLabel = new JLabel(modeNames[modeIndex]);
		
		topPanel.add(increaseHeight);
		topPanel.add(decreaseHeight);
		topPanel.add(toggleMode);
		topPanel.add(modeLabel);
		topPanel.add(exportLevel);
		topPanel.setMaximumSize(new Dimension(1080, 25));
		
		itemsPanel = new JScrollPane(innerItemsPanel);
		itemsPanel.setPreferredSize(new Dimension(800, 100));
		
//		itemsPanel.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
//		itemsPanel.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_ALWAYS);
		ic.setItemsPanel(innerItemsPanel);
		ec.setEditorPanel(innerEditorPanel);
		
		Border editorBorder = BorderFactory.createBevelBorder(BevelBorder.LOWERED);
		editorPanel.setBorder(editorBorder);
		
		Border itemsBorder = BorderFactory.createBevelBorder(BevelBorder.LOWERED);
		itemsPanel.setBorder(itemsBorder);
		
		layout = new GroupLayout(this);
		this.setLayout(layout);
		
		layout.setAutoCreateGaps(true);
		layout.setAutoCreateContainerGaps(true);
		
		GroupLayout.ParallelGroup hGroup = layout.createParallelGroup();
		hGroup
			.addComponent(topPanel)
			.addComponent(editorPanel)
			.addComponent(itemsPanel);
//		this.add(menu, BorderLayout.NORTH);
//		this.add(editorPanel, BorderLayout.CENTER);
//		this.add(itemsPanel, BorderLayout.SOUTH);
		layout.setHorizontalGroup(hGroup);
		
		GroupLayout.SequentialGroup vGroup = layout.createSequentialGroup();
		vGroup
			.addComponent(topPanel)
			.addComponent(editorPanel)
			.addComponent(itemsPanel);	   
	   	layout.setVerticalGroup(vGroup);

	}
	
	public void getReady(){
		innerItemsPanel.organizeItems();
	}
	
	public void toggleMode(){
		modeIndex = (1+modeIndex)%2;
		modeLabel.setText(modeNames[modeIndex]);
	}
	
	public void setMode(int mode){
		modeIndex = mode;
		this.modeLabel.setText(modeNames[mode]);		
	}
	
}
