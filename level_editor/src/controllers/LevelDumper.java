package controllers;

import java.util.ArrayList;
import java.util.Iterator;

import com.google.gson.Gson;

import models.Item;
import models.ItemDump;

public class LevelDumper {

	private ArrayList<ItemDump> itemDumps;
	
	public LevelDumper(){
		itemDumps = new ArrayList<ItemDump>();
	}
	
	public void dump(ArrayList<Item> items){
		
		Iterator<Item> it = items.iterator();
		while(it.hasNext()){
			Item item = it.next();
			ItemDump itemDump = new ItemDump(item);
			itemDumps.add(itemDump);			
		}
		Gson gson = new Gson();
		String json = gson.toJson(itemDumps);
		System.out.println("JSON: " + json);
	}
}
