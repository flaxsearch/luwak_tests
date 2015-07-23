package uk.co.flax.luwak_test;

import java.io.File;
import java.io.FileFilter;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.zip.GZIPInputStream;

import org.apache.commons.io.IOUtils;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.util.CharArraySet;

import uk.co.flax.luwak.InputDocument;
import uk.co.flax.luwak.Matches;
import uk.co.flax.luwak.Monitor;
import uk.co.flax.luwak.MonitorQuery;
import uk.co.flax.luwak.QueryMatch;
//import uk.co.flax.luwak.matchers.ExplainingMatch;
//import uk.co.flax.luwak.matchers.ExplainingMatcher;
import uk.co.flax.luwak.matchers.SimpleMatcher;
import uk.co.flax.luwak.presearcher.MatchAllPresearcher;
import uk.co.flax.luwak.presearcher.TermFilteredPresearcher;
import uk.co.flax.luwak.queryparsers.LuceneQueryParser;

/**
 * Luwak test class
 */
public class LuwakTester 
{
    public static void main(String[] args) throws Exception 
    {
    	CharArraySet stopwords = new CharArraySet(0, false);
    	StandardAnalyzer analyzer = new StandardAnalyzer(stopwords);
    	LuceneQueryParser parser = new LuceneQueryParser("text", analyzer);
    	Monitor monitor = new Monitor(parser, new TermFilteredPresearcher());
//    	Monitor monitor = new Monitor(parser, new MatchAllPresearcher());

    	// load the queries
    	File query_dir = new File(args[0]);
    	File[] query_files = query_dir.listFiles(new FileFilter() { 
    		public boolean accept(File f) { return f.getName().endsWith(".txt"); }
    	});

    	int count = 0;
    	for (File query_file : query_files) {
    		FileInputStream fis = new FileInputStream(query_file);
    		String query_text = IOUtils.toString(fis);
    		fis.close();
    		String query_id = query_file.getName();
    		query_id = query_id.substring(0, query_id.length() - 4);
        	MonitorQuery mq = new MonitorQuery(query_id, query_text);
        	monitor.update(mq);
        	count++;
        	if (count % 1000 == 0) {
        		System.out.println("loaded " + count + " queries");
        	}
    	}

    	int limit = 1000000;
    	if (args.length == 3) {
    		limit = Integer.parseInt(args[2]);
    	}
    	
    	long t0 = System.currentTimeMillis();
    	
    	// run the documents through the monitor
    	File doc_dir = new File(args[1]);
    	File[] doc_files = doc_dir.listFiles(new FileFilter() { 
    		public boolean accept(File f) { return f.getName().endsWith(".gz"); }
    	});
    	
    	count = 0;
    	for (File doc_file : doc_files) {
    		FileInputStream fis = new FileInputStream(doc_file);
    		String doc_text = IOUtils.toString(new GZIPInputStream(fis));
    		fis.close();
    	
        	InputDocument doc = InputDocument.builder(doc_file.getName())
        			.addField("text", doc_text, analyzer).build();
        	
        	Matches<QueryMatch> matches = monitor.match(doc, SimpleMatcher.FACTORY);
        	System.out.println(doc_file.getName() + " " + matches.getMatchCount());
        	count ++;
        	if (count == limit) break;
        	
//        	ArrayList<String> query_ids = new ArrayList<String>(matches.getMatchCount());
//        	for (QueryMatch match : matches) {
//        		query_ids.add(match.getQueryId());
//        	}
//        	Collections.sort(query_ids);
//        	for (String tmp : query_ids) {
//        		System.out.println(tmp);
//        	}
    	}
    	
    	long t1 = System.currentTimeMillis();
    	System.out.println("matched " + count + " docs in " + (t1 - t0) + " ms (" +
    	    String.format("%.2f", count * 1000.0 / (t1 - t0)) + " docs/s)");
    	
    	monitor.close();
    }
}
