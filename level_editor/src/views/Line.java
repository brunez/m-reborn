package views;

public class Line{
	
	private int originX;
	private int originY;
	private int endX;
	private int endY;
	
	public Line(){
		originX = 0;
		originY = 0;
		endX = 0;
		endY = 0;
	}

	public int getOriginX() {
		return originX;
	}

	public void setOriginX(int originX) {
		this.originX = originX;
	}

	public int getOriginY() {
		return originY;
	}

	public void setOriginY(int originY) {
		this.originY = originY;
	}

	public int getEndX() {
		return endX;
	}

	public void setEndX(int endX) {
		this.endX = endX;
	}

	public int getEndY() {
		return endY;
	}

	public void setEndY(int endY) {
		this.endY = endY;
	}
	
	public int getLength(){
		int xLength = Math.abs(endX - originX);
		int yLength = Math.abs(endY - originY);
		if(xLength > yLength){
			return xLength;
		} else {
			return yLength;
		}
	}
		
}
