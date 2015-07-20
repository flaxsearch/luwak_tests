package uk.co.flax.luwak_test;

import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;

import uk.co.flax.luwak.InputDocument;
import uk.co.flax.luwak.Matches;
import uk.co.flax.luwak.Monitor;
import uk.co.flax.luwak.MonitorQuery;
import uk.co.flax.luwak.QueryMatch;
import uk.co.flax.luwak.matchers.SimpleMatcher;
import uk.co.flax.luwak.presearcher.TermFilteredPresearcher;
import uk.co.flax.luwak.queryparsers.LuceneQueryParser;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main(String[] args ) throws IOException 
    {
    	Monitor monitor = new Monitor(new LuceneQueryParser("text"), new TermFilteredPresearcher());

    	MonitorQuery mq = new MonitorQuery("query1", "text:banana");
    	monitor.update(mq);

    	InputDocument doc = InputDocument.builder("doc1")
    			.addField("text", "apple banana lemon", new StandardAnalyzer())
    	        .build();
    	
    	Matches<QueryMatch> matches = monitor.match(doc, SimpleMatcher.FACTORY);
    	System.out.println("got " + matches.getMatchCount() + " matches");
    	monitor.close();
    }
}
