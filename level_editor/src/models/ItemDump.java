package models;

/**
 * 
 * @author bruno
 *
 */
public class ItemDump {

	private String c;
	private int x;
	private int y;
	int e;	
	
	/**
	 * 
	 * @param item
	 */
	public ItemDump(Item item) {
		super();
		this.x = item.getPosX();
		this.y = item.getPosY();
		this.e = item.getItemType().getCorrection();
		//Python seems to precede class names 
		//with __main__ when it pickles objects
		this.c = item.getItemType().getName();
	}

}
